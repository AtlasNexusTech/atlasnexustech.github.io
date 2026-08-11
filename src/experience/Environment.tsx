import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import type { SceneSystemProps } from './types'
import { range } from '../lib/config'

export function Environment({ progressRef, reducedMotion }: SceneSystemProps) {
  const light = useRef<THREE.PointLight>(null)

  useFrame(({ clock }) => {
    if (!light.current) return
    const activity = range(progressRef.current, 0.24, 0.56)
    const pulse = reducedMotion ? 0 : Math.sin(clock.elapsedTime * 0.55) * 0.08
    light.current.intensity = 4.2 + activity * 1.3 + pulse
  })

  return (
    <>
      <ambientLight intensity={0.16} />
      <pointLight ref={light} position={[2.5, 2.8, 4]} intensity={4.2} color="#438dff" distance={13} decay={2} />
      <pointLight position={[-4, -2, 2]} intensity={1.5} color="#d8e7ff" distance={10} decay={2} />
    </>
  )
}
