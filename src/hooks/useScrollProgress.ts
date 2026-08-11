import { useEffect, useRef, useState } from 'react'
import type { MutableRefObject } from 'react'
import { clamp } from '../lib/config'

export interface ScrollState {
  progressRef: MutableRefObject<number>
  activeScene: number
  hasScrolled: boolean
}

export function useScrollProgress(sceneCount: number): ScrollState {
  const progressRef = useRef(0)
  const [activeScene, setActiveScene] = useState(0)
  const [hasScrolled, setHasScrolled] = useState(false)

  useEffect(() => {
    let frame = 0
    const update = () => {
      frame = 0
      const max = Math.max(1, document.documentElement.scrollHeight - window.innerHeight)
      const progress = clamp(window.scrollY / max)
      progressRef.current = progress
      setHasScrolled(progress > 0.012)
      setActiveScene(Math.min(sceneCount - 1, Math.floor(progress * sceneCount + 0.22)))
      document.documentElement.style.setProperty('--page-progress', progress.toFixed(4))
    }
    const requestUpdate = () => {
      if (!frame) frame = window.requestAnimationFrame(update)
    }
    update()
    window.addEventListener('scroll', requestUpdate, { passive: true })
    window.addEventListener('resize', requestUpdate)
    return () => {
      window.removeEventListener('scroll', requestUpdate)
      window.removeEventListener('resize', requestUpdate)
      if (frame) window.cancelAnimationFrame(frame)
    }
  }, [sceneCount, progressRef])

  return { progressRef, activeScene, hasScrolled }
}
