import { PRIMARY_CTA } from '../lib/content'

interface NavigationProps {
  visible: boolean
}

export function Navigation({ visible }: NavigationProps) {
  return (
    <header className={`site-header ${visible ? 'site-header--visible' : ''}`}>
      <a className="brand" href="#top" aria-label="Atlas Nexus — retour en haut">
        <span className="brand-mark"><img src="/atlas-logo.png" alt="" /></span>
        <span>Atlas Nexus</span>
        <small>BETA</small>
      </a>
      <nav aria-label="Navigation principale">
        <a href="#approach">Approche</a>
        <a href="#systems">Systèmes</a>
        <a className="nav-cta" href={PRIMARY_CTA.href}>Diagnostic</a>
      </nav>
      <a className="production-link" href="https://atlasnexus.tech/">Site actuel ↗</a>
    </header>
  )
}
