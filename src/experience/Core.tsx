import { useMemo, useRef } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'
import type { SceneSystemProps } from './types'
import { PALETTE, range } from '../lib/config'

const vertexShader = /* glsl */ `
uniform float uTime;
uniform float uProgress;
varying vec3 vNormalView;
varying float vPulse;
void main() {
  float wave = sin(position.y * 5.0 + uTime * 0.55) * 0.018;
  wave += sin(position.x * 4.0 - uTime * 0.32) * 0.012;
  vec3 displaced = position + normal * wave * (0.45 + uProgress);
  vNormalView = normalize(normalMatrix * normal);
  vPulse = wave;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(displaced, 1.0);
}`

const fragmentShader = /* glsl */ `
uniform vec3 uColor;
uniform float uProgress;
varying vec3 vNormalView;
varying float vPulse;
void main() {
  float fresnel = pow(1.0 - abs(vNormalView.z), 2.35);
  float inner = 0.16 + fresnel * 0.75 + vPulse * 2.0;
  vec3 color = uColor * inner + vec3(0.18, 0.38, 0.75) * fresnel * (0.35 + uProgress * 0.25);
  gl_FragColor = vec4(color, 0.84 + fresnel * 0.14);
}`

export function Core({ progressRef, profile, reducedMotion }: SceneSystemProps) {
  const group = useRef<THREE.Group>(null)
  const material = useRef<THREE.ShaderMaterial>(null)
  const { viewport } = useThree()
  const mobile = profile === 'MOBILE'
  const detail = profile === 'HIGH' ? 4 : profile === 'MEDIUM' ? 3 : 2
  const uniforms = useMemo(() => ({
    uTime: { value: 0 },
    uProgress: { value: 0 },
    uColor: { value: new THREE.Color(PALETTE.blue) },
  }), [])

  useFrame(({ clock }, delta) => {
    const progress = progressRef.current
    if (material.current) {
      material.current.uniforms.uTime.value = reducedMotion ? 0 : clock.elapsedTime
      material.current.uniforms.uProgress.value = progress
    }
    if (group.current) {
      const endCalm = range(progress, 0.82, 1)
      const targetX = mobile || viewport.width < 7 ? 0 : 1.55 - endCalm * 1.55
      const targetY = mobile ? 1.35 - progress * 0.32 : 0.1 - endCalm * 0.1
      group.current.position.x = THREE.MathUtils.damp(group.current.position.x, targetX, 3.2, delta)
      group.current.position.y = THREE.MathUtils.damp(group.current.position.y, targetY, 3.2, delta)
      const scale = 0.84 + range(progress, 0.1, 0.42) * 0.28 - endCalm * 0.34
      group.current.scale.setScalar(THREE.MathUtils.damp(group.current.scale.x, scale, 3, delta))
      if (!reducedMotion) group.current.rotation.y += delta * 0.035
    }
  })

  return (
    <group ref={group}>
      <mesh>
        <icosahedronGeometry args={[1.04, detail]} />
        <shaderMaterial
          ref={material}
          vertexShader={vertexShader}
          fragmentShader={fragmentShader}
          uniforms={uniforms}
          transparent
          depthWrite={false}
        />
      </mesh>
      <mesh scale={1.1}>
        <icosahedronGeometry args={[1.04, 2]} />
        <meshBasicMaterial color={PALETTE.ice} transparent opacity={0.09} wireframe depthWrite={false} />
      </mesh>
      <mesh rotation={[Math.PI * 0.5, 0.3, 0]}>
        <torusGeometry args={[1.38, 0.006, 4, 128]} />
        <meshBasicMaterial color={PALETTE.blue} transparent opacity={0.32} depthWrite={false} />
      </mesh>
    </group>
  )
}
