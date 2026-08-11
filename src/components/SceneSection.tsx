import type { ReactNode } from 'react'

interface SceneSectionProps {
  id: string
  label: string
  title: string
  children: ReactNode
  align?: 'left' | 'right'
}

export function SceneSection({ id, label, title, children, align = 'left' }: SceneSectionProps) {
  return (
    <section id={id} className={`scene scene--${align}`} aria-labelledby={`${id}-title`}>
      <div className="scene-copy">
        <p className="technical-label">{label}</p>
        <h2 id={`${id}-title`}>{title}</h2>
        <div className="scene-body">{children}</div>
      </div>
    </section>
  )
}
