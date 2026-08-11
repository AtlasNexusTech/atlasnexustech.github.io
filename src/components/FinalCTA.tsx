import { PRIMARY_CTA } from '../lib/content'

export function FinalCTA() {
  return (
    <section id="contact" className="final-cta" aria-labelledby="contact-title">
      <div className="final-cta__inner scene-copy">
        <p className="technical-label">SCENE 06 / ACT</p>
        <h2 id="contact-title">Commencez par trente minutes utiles.</h2>
        <p>Identifions ce qui mange vos semaines et ce qu’un agent peut réellement reprendre. Vous repartez avec un plan clair.</p>
        <a className="primary-cta" href={PRIMARY_CTA.href}>
          <span>{PRIMARY_CTA.label}</span>
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6" /></svg>
        </a>
        <small>Le diagnostic se poursuit sur le site principal Atlas Nexus.</small>
      </div>
    </section>
  )
}
