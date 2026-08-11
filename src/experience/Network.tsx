import { useMemo, useRef } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'
import type { SceneSystemProps } from './types'
import { PALETTE, QUALITY_SETTINGS, range } from '../lib/config'

function seeded(seed: number) {
  let value = seed >>> 0
  return () => {
    value = (value * 1103515245 + 12345) >>> 0
    return value / 4294967296
  }
}

export function Network({ progressRef, profile, selectedStation, reducedMotion }: SceneSystemProps) {
  const meshRef = useRef<THREE.InstancedMesh>(null)
  const lineGeometry = useRef<THREE.BufferGeometry>(null)
  const signalGeometry = useRef<THREE.BufferGeometry>(null)
  const lineMaterial = useRef<THREE.LineBasicMaterial>(null)
  const signalMaterial = useRef<THREE.PointsMaterial>(null)
  const root = useRef<THREE.Group>(null)
  const { viewport } = useThree()
  const settings = QUALITY_SETTINGS[profile]
  const mobile = profile === 'MOBILE'
  const count = settings.nodes
  const signalCount = settings.signals

  const layout = useMemo(() => {
    const random = seeded(42042)
    return Array.from({ length: count }, (_, index) => {
      if (index === 0) return new THREE.Vector3(0, 0, 0)
      const theta = index * 2.399963 + random() * 0.12
      const radius = 1.5 + random() * 1.45
      return new THREE.Vector3(
        Math.cos(theta) * radius,
        (random() - 0.5) * 3.2,
        Math.sin(theta) * radius * 0.72,
      )
    })
  }, [count])

  const current = useMemo(() => layout.map(() => new THREE.Vector3()), [layout])
  const edges = useMemo(() => {
    const values: Array<[number, number]> = []
    for (let i = 1; i < count; i += 1) {
      values.push([i, Math.max(0, Math.floor((i - 1) * 0.48))])
      if (i > 5 && i % 3 === 0) values.push([i, (i + 4) % count])
    }
    return values
  }, [count])
  const linePositions = useMemo(() => new Float32Array(edges.length * 6), [edges.length])
  const signalPositions = useMemo(() => new Float32Array(signalCount * 3), [signalCount])
  const matrix = useMemo(() => new THREE.Matrix4(), [])
  const color = useMemo(() => new THREE.Color(), [])
  const warmColor = useMemo(() => new THREE.Color(PALETTE.warm), [])
  const blueColor = useMemo(() => new THREE.Color(PALETTE.blue), [])
  const dimColor = useMemo(() => new THREE.Color('#20304a'), [])

  useFrame(({ clock }, delta) => {
    if (!meshRef.current || !root.current) return
    const progress = progressRef.current
    const deploy = range(progress, 0.08, 0.34)
    const control = range(progress, 0.46, 0.66)
    const endCalm = range(progress, 0.82, 1)
    const spread = 0.56 + deploy * 0.66 - endCalm * 0.22
    const activity = range(progress, 0.25, 0.48) * (1 - endCalm * 0.78)
    const selectedNode = Math.min(count - 1, selectedStation + 2)

    for (let i = 0; i < count; i += 1) {
      const base = layout[i]
      const drift = reducedMotion ? 0 : Math.sin(clock.elapsedTime * 0.22 + i * 1.7) * 0.045 * activity
      current[i].set(base.x * spread, base.y * spread + drift, base.z * spread)
      if (control > 0 && i > 0) current[i].lerp(layout[1], control * 0.035)
      const selected = progress > 0.66 && i === selectedNode
      const scale = i === 0 ? 0.15 : selected ? 0.18 : 0.075 + deploy * 0.035
      matrix.makeScale(scale, scale, scale)
      matrix.setPosition(current[i])
      meshRef.current.setMatrixAt(i, matrix)
      if (control > 0.28 && i === 1) color.copy(warmColor)
      else if (progress > 0.66 && !selected && i > 1) color.copy(dimColor)
      else color.copy(blueColor)
      meshRef.current.setColorAt(i, color)
    }
    meshRef.current.instanceMatrix.needsUpdate = true
    if (meshRef.current.instanceColor) meshRef.current.instanceColor.needsUpdate = true

    const lineAttribute = lineGeometry.current?.attributes.position as THREE.BufferAttribute | undefined
    if (lineAttribute) {
      let cursor = 0
      for (const [a, b] of edges) {
        linePositions[cursor++] = current[a].x
        linePositions[cursor++] = current[a].y
        linePositions[cursor++] = current[a].z
        linePositions[cursor++] = current[b].x
        linePositions[cursor++] = current[b].y
        linePositions[cursor++] = current[b].z
      }
      lineAttribute.needsUpdate = true
    }
    if (lineMaterial.current) lineMaterial.current.opacity = 0.05 + deploy * 0.22 - endCalm * 0.13

    const signalAttribute = signalGeometry.current?.attributes.position as THREE.BufferAttribute | undefined
    if (signalAttribute) {
      for (let i = 0; i < signalCount; i += 1) {
        const edge = edges[(i * 3) % edges.length]
        const phase = (clock.elapsedTime * (0.055 + (i % 3) * 0.012) + i / signalCount) % 1
        const from = current[edge[0]]
        const to = current[edge[1]]
        signalPositions[i * 3] = THREE.MathUtils.lerp(from.x, to.x, phase)
        signalPositions[i * 3 + 1] = THREE.MathUtils.lerp(from.y, to.y, phase)
        signalPositions[i * 3 + 2] = THREE.MathUtils.lerp(from.z, to.z, phase)
      }
      signalAttribute.needsUpdate = true
    }
    if (signalMaterial.current) signalMaterial.current.opacity = activity * 0.85

    const endX = endCalm * (mobile ? 0 : -0.45)
    const targetX = mobile || viewport.width < 7 ? 0 : 1.55 + endX
    const targetY = mobile ? 1.35 - progress * 0.32 : 0.1
    root.current.position.x = THREE.MathUtils.damp(root.current.position.x, targetX, 3.2, delta)
    root.current.position.y = THREE.MathUtils.damp(root.current.position.y, targetY, 3.2, delta)
    if (!reducedMotion) root.current.rotation.y += delta * 0.018
  })

  return (
    <group ref={root}>
      <instancedMesh ref={meshRef} args={[undefined, undefined, count]} frustumCulled={false}>
        <sphereGeometry args={[1, profile === 'HIGH' ? 10 : 6, profile === 'HIGH' ? 10 : 6]} />
        <meshBasicMaterial vertexColors transparent opacity={0.95} toneMapped={false} />
      </instancedMesh>
      <lineSegments frustumCulled={false}>
        <bufferGeometry ref={lineGeometry}>
          <bufferAttribute attach="attributes-position" args={[linePositions, 3]} />
        </bufferGeometry>
        <lineBasicMaterial ref={lineMaterial} color="#79aaff" transparent opacity={0.12} depthWrite={false} />
      </lineSegments>
      <points frustumCulled={false}>
        <bufferGeometry ref={signalGeometry}>
          <bufferAttribute attach="attributes-position" args={[signalPositions, 3]} />
        </bufferGeometry>
        <pointsMaterial ref={signalMaterial} color="#f3f7ff" size={mobile ? 0.055 : 0.075} transparent opacity={0} depthWrite={false} blending={THREE.AdditiveBlending} />
      </points>
    </group>
  )
}
