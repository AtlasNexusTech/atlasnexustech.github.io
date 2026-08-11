import { useEffect, useRef } from 'react'
import * as THREE from 'three'

export function usePointerInput(enabled: boolean) {
  const pointerRef = useRef(new THREE.Vector2())

  useEffect(() => {
    if (!enabled) return
    const update = (event: PointerEvent) => {
      pointerRef.current.set(
        (event.clientX / window.innerWidth) * 2 - 1,
        -(event.clientY / window.innerHeight) * 2 + 1,
      )
    }
    const reset = () => pointerRef.current.set(0, 0)
    window.addEventListener('pointermove', update, { passive: true })
    window.addEventListener('pointerleave', reset)
    return () => {
      window.removeEventListener('pointermove', update)
      window.removeEventListener('pointerleave', reset)
    }
  }, [enabled])

  return pointerRef
}
