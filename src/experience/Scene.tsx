import type { SceneSystemProps } from './types'
import { CameraRig } from './CameraRig'
import { Core } from './Core'
import { Environment } from './Environment'
import { Network } from './Network'
import { ParticleField } from './ParticleField'

export function Scene(props: SceneSystemProps) {
  return (
    <>
      <color attach="background" args={['#05070b']} />
      <fog attach="fog" args={['#05070b', 8, 23]} />
      <CameraRig {...props} />
      <Environment {...props} />
      <ParticleField {...props} />
      <Network {...props} />
      <Core {...props} />
    </>
  )
}
