import type { CSSProperties } from 'react'
import { USE_CASES } from '../lib/content'

interface UseCaseSystemsProps {
  selected: number
  onSelect: (index: number) => void
}

export function UseCaseSystems({ selected, onSelect }: UseCaseSystemsProps) {
  const current = USE_CASES[selected]
  return (
    <section id="systems" className="systems" aria-labelledby="systems-title">
      <div className="systems-shell">
        <div className="systems-heading" data-reveal>
          <p className="technical-label">CAPABILITIES / 01–05</p>
          <h2 id="systems-title">Des capacités reliées à votre activité.</h2>
          <p>Explorez les stations du réseau. Chaque système correspond à un besoin déjà présent dans l’offre Atlas Nexus.</p>
        </div>
        <div className="station-interface">
          <div className="station-rail" role="tablist" aria-label="Cas d’usage Atlas Nexus" style={{ '--station': selected } as CSSProperties}>
            {USE_CASES.map((item, index) => (
              <button
                key={item.id}
                type="button"
                role="tab"
                aria-selected={selected === index}
                aria-controls="station-detail"
                className={selected === index ? 'is-active' : ''}
                onClick={() => onSelect(index)}
              >
                <span>{String(index + 1).padStart(2, '0')}</span>
                <strong>{item.id}</strong>
              </button>
            ))}
          </div>
          <article id="station-detail" className="station-detail" role="tabpanel" aria-live="polite" key={current.id}>
            <p className="technical-label">{current.label}</p>
            <h3>{current.title}</h3>
            <p>{current.description}</p>
            <div className="station-proof"><i aria-hidden="true" />{current.proof}</div>
          </article>
        </div>
      </div>
    </section>
  )
}
