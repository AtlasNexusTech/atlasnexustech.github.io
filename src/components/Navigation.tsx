import { PRIMARY_CTA, SCENES } from '../lib/content'

interface NavigationProps {
  activeScene: number
  visible: boolean
}

export function Navigation({ activeScene, visible }: NavigationProps) {
  return (
    <header className={`site-header ${visible ? 'site-header--visible' : ''}`}>
      <a className="brand" href="#core" aria-label="Atlas Nexus — revenir au noyau">
        <span className="brand-mark"><img src="/atlas-logo.png" alt="" /></span>
        <span>Atlas Nexus</span>
        <small>BETA</small>
      </a>
      <nav aria-label="Navigation principale">
        <a href="#deploy">Déployer</a>
        <a href="#systems">Systèmes</a>
        <a className="nav-cta" href={PRIMARY_CTA.href}>Diagnostic</a>
      </nav>
      <div className="scene-status" aria-hidden="true">
        <span>{String(activeScene + 1).padStart(2, '0')}</span>
        <i />
        <span>{String(SCENES.length).padStart(2, '0')}</span>
      </div>
    </header>
  )
}
