import { Suspense } from 'react'
import { Canvas } from '@react-three/fiber'
import { AdaptiveDpr } from '@react-three/drei'
import type { ExperienceProps } from './types'
import { QUALITY_SETTINGS } from '../lib/config'
import { FrameGovernor } from './FrameGovernor'
import { Scene } from './Scene'

export function Experience({ onQualityDecline, ...sceneProps }: ExperienceProps) {
  const settings = QUALITY_SETTINGS[sceneProps.profile]
  return (
    <div className="experience-layer" aria-hidden="true">
      <Canvas
        dpr={[Math.min(0.8, settings.maxDpr), settings.maxDpr]}
        camera={{ position: [0, 0, 9.2], fov: sceneProps.profile === 'MOBILE' ? 52 : 45, near: 0.1, far: 40 }}
        gl={{ antialias: sceneProps.profile === 'HIGH', alpha: false, powerPreference: 'high-performance', stencil: false }}
        onCreated={({ gl }) => {
          gl.outputColorSpace = 'srgb'
          gl.toneMapping = 3
          gl.toneMappingExposure = 0.82
        }}
      >
        <Suspense fallback={null}>
          <FrameGovernor profile={sceneProps.profile} onDecline={onQualityDecline} />
          <Scene {...sceneProps} />
          <AdaptiveDpr pixelated={false} />
        </Suspense>
      </Canvas>
    </div>
  )
}
