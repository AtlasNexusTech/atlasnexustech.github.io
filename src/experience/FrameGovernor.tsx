import { useEffect, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import type { QualityProfile } from '../lib/config'

interface FrameGovernorProps {
  profile: QualityProfile
  onDecline: () => void
}

export function FrameGovernor({ profile, onDecline }: FrameGovernorProps) {
  const warmup = useRef(0)
  const frames = useRef(0)
  const elapsed = useRef(0)
  const decided = useRef(false)

  useEffect(() => {
    warmup.current = 0
    frames.current = 0
    elapsed.current = 0
    decided.current = false
  }, [profile])

  useFrame((_, delta) => {
    if (decided.current || profile === 'LOW' || profile === 'MOBILE') return
    if (warmup.current < 75) {
      warmup.current += 1
      return
    }
    frames.current += 1
    elapsed.current += Math.min(delta, 0.1)
    if (frames.current >= 120) {
      decided.current = true
      const averageFrameMs = (elapsed.current / frames.current) * 1000
      if (averageFrameMs > 21.5) onDecline()
    }
  })

  return null
}
