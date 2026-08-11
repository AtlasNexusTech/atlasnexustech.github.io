import { useMemo, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import type { SceneSystemProps } from './types'
import { QUALITY_SETTINGS, range } from '../lib/config'

function seeded(seed: number) {
  let value = seed >>> 0
  return () => {
    value = (value * 1664525 + 1013904223) >>> 0
    return value / 4294967296
  }
}

export function ParticleField({ progressRef, profile, reducedMotion }: SceneSystemProps) {
  const group = useRef<THREE.Points>(null)
  const settings = QUALITY_SETTINGS[profile]
  const positions = useMemo(() => {
    const random = seeded(90617)
    const values = new Float32Array(settings.particles * 3)
    for (let i = 0; i < settings.particles; i += 1) {
      const radius = 4.8 + random() * 12
      const theta = random() * Math.PI * 2
      const phi = Math.acos(2 * random() - 1)
      values[i * 3] = radius * Math.sin(phi) * Math.cos(theta)
      values[i * 3 + 1] = radius * Math.cos(phi) * 0.65
      values[i * 3 + 2] = radius * Math.sin(phi) * Math.sin(theta)
    }
    return values
  }, [settings.particles])

  useFrame((_, delta) => {
    if (!group.current || reducedMotion) return
    const calm = range(progressRef.current, 0.82, 1)
    group.current.rotation.y += delta * (0.006 - calm * 0.004)
    group.current.rotation.x += delta * 0.0015
  })

  return (
    <points ref={group} frustumCulled={false}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" args={[positions, 3]} />
      </bufferGeometry>
      <pointsMaterial
        color="#8fbaff"
        size={profile === 'MOBILE' ? 0.018 : 0.024}
        sizeAttenuation
        transparent
        opacity={0.33}
        depthWrite={false}
        blending={THREE.AdditiveBlending}
      />
    </points>
  )
}
