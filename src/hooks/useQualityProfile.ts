import { useEffect, useState } from 'react'
import type { QualityProfile } from '../lib/config'

interface NavigatorWithMemory extends Navigator {
  deviceMemory?: number
}

export function useQualityProfile() {
  const [profile, setProfile] = useState<QualityProfile>('MEDIUM')

  useEffect(() => {
    const nav = navigator as NavigatorWithMemory
    const mobile = window.matchMedia('(max-width: 700px), (pointer: coarse)').matches
    if (mobile) {
      setProfile('MOBILE')
      return
    }
    const memory = nav.deviceMemory ?? 4
    const cores = navigator.hardwareConcurrency ?? 4
    if (memory >= 8 && cores >= 8) setProfile('HIGH')
    else if (memory <= 2 || cores <= 2) setProfile('LOW')
    else setProfile('MEDIUM')
  }, [])

  return { profile, setProfile }
}
