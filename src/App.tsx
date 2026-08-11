import { lazy, Suspense, useEffect, useMemo, useState } from 'react'
import { Navigation } from './components/Navigation'
import { SceneSection } from './components/SceneSection'
import { UseCaseSystems } from './components/UseCaseSystems'
import { FinalCTA } from './components/FinalCTA'
import { ScrollIndicator } from './components/ScrollIndicator'
import { WebGLFallback } from './components/WebGLFallback'
import { usePointerInput } from './hooks/usePointerInput'
import { useQualityProfile } from './hooks/useQualityProfile'
import { useReducedMotion } from './hooks/useReducedMotion'
import { useScrollProgress } from './hooks/useScrollProgress'
import { SCENES } from './lib/content'
import { supportsWebGL } from './lib/webgl'
import type { QualityProfile } from './lib/config'

const Experience = lazy(() => import('./experience/Experience').then((module) => ({ default: module.Experience })))

const downgrade: Record<QualityProfile, QualityProfile> = {
  HIGH: 'MEDIUM', MEDIUM: 'LOW', LOW: 'LOW', MOBILE: 'MOBILE',
}

export default function App() {
  const reducedMotion = useReducedMotion()
  const { profile, setProfile } = useQualityProfile()
  const { progressRef, activeScene, hasScrolled } = useScrollProgress(SCENES.length)
  const pointerRef = usePointerInput(!reducedMotion && profile !== 'MOBILE')
  const [selectedStation, setSelectedStation] = useState(0)
  const webglAvailable = useMemo(() => supportsWebGL(), [])

  useEffect(() => {
    const elements = Array.from(document.querySelectorAll<HTMLElement>('.scene-copy'))
    if (reducedMotion) {
      elements.forEach((element) => element.classList.add('is-visible'))
      return
    }
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) (entry.target as HTMLElement).classList.add('is-visible')
      })
    }, { threshold: 0.2, rootMargin: '0px 0px -12% 0px' })
    elements.forEach((element) => observer.observe(element))
    return () => observer.disconnect()
  }, [reducedMotion])

  return (
    <div className="app-shell" data-quality={profile} data-reduced-motion={reducedMotion ? 'true' : 'false'}>
      <a className="skip-link" href="#core">Aller au contenu</a>
      <Navigation activeScene={activeScene} visible={hasScrolled} />
      {webglAvailable ? (
        <Suspense fallback={null}>
          <Experience
            progressRef={progressRef}
            pointerRef={pointerRef}
            profile={reducedMotion && profile === 'HIGH' ? 'MEDIUM' : profile}
            reducedMotion={reducedMotion}
            selectedStation={selectedStation}
            onQualityDecline={() => setProfile((current) => downgrade[current])}
          />
        </Suspense>
      ) : <WebGLFallback />}
      <div className="atmosphere" aria-hidden="true" />
      <div className="progress-line" aria-hidden="true"><i /></div>
      <ScrollIndicator hidden={hasScrolled} />

      <main className="story">
        <section id="core" className="hero" aria-labelledby="hero-title">
          <div className="hero-copy scene-copy is-visible">
            <p className="technical-label">AI AGENT INFRASTRUCTURE / BETA</p>
            <h1 id="hero-title">ATLAS<br />NEXUS</h1>
            <p className="hero-tagline">Deploy. Automate. Operate.</p>
            <p className="hero-intro">Je vous aide à faire travailler l’Intelligence pour vous&nbsp;: je déploie vos agents, je les configure sur votre infrastructure et je veille à ce qu’ils tournent dans la durée.</p>
            <a className="text-link" href="#deploy">Entrer dans l’infrastructure <span aria-hidden="true">↘</span></a>
          </div>
        </section>

        <SceneSection id="deploy" label="SCENE 02 / DEPLOY" title="Vos agents, installés chez vous." align="left">
          <p>Votre premier agent prend en charge une tâche réelle&nbsp;: mails, relances ou rapports.</p>
          <p className="scene-emphasis">Sur votre machine ou un VPS. Démontré en direct. Documenté pour rester à vous.</p>
        </SceneSection>

        <SceneSection id="automate" label="SCENE 03 / AUTOMATE" title="L’activité circule. Vous récupérez du temps." align="right">
          <p>Les agents traitent vos mails, vos devis, vos relances et vos rapports. Mémoire, outils et compétences coopèrent sans ajouter un SaaS de plus.</p>
          <p className="scene-emphasis">Les signaux avancent. Les étapes sensibles attendent votre validation.</p>
        </SceneSection>

        <SceneSection id="control" label="SCENE 04 / CONTROL" title="L’IA prépare et exécute. Vous gardez le contrôle." align="left">
          <p>Vous validez, ils exécutent. Les sorties convergent vers des décisions lisibles plutôt que vers une boîte noire.</p>
          <ul className="control-list">
            <li><span>01</span>Code et documentation accessibles</li>
            <li><span>02</span>Formats ouverts et données maîtrisées</li>
            <li><span>03</span>Supervision et évolution continues</li>
          </ul>
        </SceneSection>

        <UseCaseSystems selected={selectedStation} onSelect={setSelectedStation} />
        <FinalCTA />
      </main>

      <footer className="beta-footer">
        <span>© 2026 Atlas Nexus</span>
        <span>Immersive beta · noindex</span>
        <a href="https://atlasnexus.tech/">Site principal</a>
      </footer>
    </div>
  )
}
