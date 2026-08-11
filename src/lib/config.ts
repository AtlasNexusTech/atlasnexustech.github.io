export type QualityProfile = 'HIGH' | 'MEDIUM' | 'LOW' | 'MOBILE'

export interface QualitySettings {
  particles: number
  nodes: number
  signals: number
  maxDpr: number
  pointerStrength: number
}

export const QUALITY_SETTINGS: Record<QualityProfile, QualitySettings> = {
  HIGH: { particles: 2200, nodes: 20, signals: 14, maxDpr: 1.5, pointerStrength: 1 },
  MEDIUM: { particles: 1000, nodes: 16, signals: 10, maxDpr: 1.15, pointerStrength: 0.75 },
  LOW: { particles: 420, nodes: 12, signals: 6, maxDpr: 0.5, pointerStrength: 0.5 },
  MOBILE: { particles: 280, nodes: 10, signals: 5, maxDpr: 0.9, pointerStrength: 0.3 },
}

export const SCENE_MARKERS = {
  core: 0,
  deploy: 0.18,
  automate: 0.36,
  control: 0.54,
  systems: 0.7,
  contact: 0.9,
} as const

export const PALETTE = {
  graphite: '#05070b',
  blue: '#3486ff',
  ice: '#b7d4ff',
  warm: '#f1e8d8',
  white: '#f4f6fb',
} as const

export const clamp = (value: number, min = 0, max = 1) => Math.min(max, Math.max(min, value))
export const smooth = (value: number) => {
  const t = clamp(value)
  return t * t * (3 - 2 * t)
}
export const range = (value: number, start: number, end: number) => smooth((value - start) / (end - start))
