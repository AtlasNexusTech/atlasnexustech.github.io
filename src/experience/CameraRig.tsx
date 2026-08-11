import { useMemo } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'
import type { SceneSystemProps } from './types'
import { QUALITY_SETTINGS, range } from '../lib/config'

export function CameraRig({ progressRef, pointerRef, profile, reducedMotion, selectedStation }: SceneSystemProps) {
  const { camera } = useThree()
  const target = useMemo(() => new THREE.Vector3(), [])
  const look = useMemo(() => new THREE.Vector3(), [])
  const settings = QUALITY_SETTINGS[profile]

  useFrame((_, delta) => {
    const progress = progressRef.current
    const deploy = range(progress, 0.08, 0.34)
    const systems = range(progress, 0.62, 0.8)
    const endCalm = range(progress, 0.82, 1)
    const pointerScale = reducedMotion ? 0 : settings.pointerStrength
    const px = pointerRef.current.x * 0.23 * pointerScale
    const py = pointerRef.current.y * 0.16 * pointerScale
    const stationOffset = systems * (selectedStation - 2) * 0.055

    target.set(
      px + stationOffset,
      py * 0.65,
      9.2 - deploy * 2.1 + endCalm * 1.6,
    )
    camera.position.x = THREE.MathUtils.damp(camera.position.x, target.x, 2.2, delta)
    camera.position.y = THREE.MathUtils.damp(camera.position.y, target.y, 2.2, delta)
    camera.position.z = THREE.MathUtils.damp(camera.position.z, target.z, 2.2, delta)
    look.set(
      (profile === 'MOBILE' ? 0 : 0.55) * (1 - endCalm),
      profile === 'MOBILE' ? 0.85 - progress * 0.25 : 0,
      0,
    )
    camera.lookAt(look)
  })

  return null
}
