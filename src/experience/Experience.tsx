import { Suspense, useEffect, useRef, useState } from 'react'
import { Canvas } from '@react-three/fiber'
import { AdaptiveDpr } from '@react-three/drei'
import type { ExperienceProps } from './types'
import { QUALITY_SETTINGS } from '../lib/config'
import { FrameGovernor } from './FrameGovernor'
import { Scene } from './Scene'

export function Experience({ onQualityDecline, ...sceneProps }: ExperienceProps) {
  const wrapper = useRef<HTMLDivElement>(null)
  const [active, setActive] = useState(true)
  const settings = QUALITY_SETTINGS[sceneProps.profile]

  useEffect(() => {
    if (!wrapper.current) return
    const observer = new IntersectionObserver(([entry]) => setActive(entry.isIntersecting), { rootMargin: '120px' })
    observer.observe(wrapper.current)
    return () => observer.disconnect()
  }, [])

  return (
    <div ref={wrapper} className="hero-experience" aria-hidden="true">
      <Canvas
        frameloop={active && !sceneProps.reducedMotion ? 'always' : 'demand'}
        dpr={[Math.min(0.8, settings.maxDpr), settings.maxDpr]}
        camera={{ position: [0, 0, 9.2], fov: sceneProps.profile === 'MOBILE' ? 50 : 43, near: 0.1, far: 40 }}
        gl={{ antialias: sceneProps.profile === 'HIGH', alpha: false, powerPreference: 'high-performance', stencil: false }}
        onCreated={({ gl }) => {
          gl.outputColorSpace = 'srgb'
          gl.toneMapping = 3
          gl.toneMappingExposure = 0.78
        }}
      >
        <Suspense fallback={null}>
          {active && !sceneProps.reducedMotion && <FrameGovernor profile={sceneProps.profile} onDecline={onQualityDecline} />}
          <Scene {...sceneProps} />
          <AdaptiveDpr pixelated={false} />
        </Suspense>
      </Canvas>
    </div>
  )
}
