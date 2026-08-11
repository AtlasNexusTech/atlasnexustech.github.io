import type { MutableRefObject } from 'react'
import type { Vector2 } from 'three'
import type { QualityProfile } from '../lib/config'

export interface ExperienceProps {
  progressRef: MutableRefObject<number>
  pointerRef: MutableRefObject<Vector2>
  profile: QualityProfile
  reducedMotion: boolean
  selectedStation: number
  onQualityDecline: () => void
}

export interface SceneSystemProps extends Omit<ExperienceProps, 'onQualityDecline'> {}
