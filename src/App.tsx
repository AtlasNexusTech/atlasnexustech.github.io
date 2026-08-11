import { lazy, Suspense, useEffect, useMemo, useState } from 'react'
import { Navigation } from './components/Navigation'
import { UseCaseSystems } from './components/UseCaseSystems'
import { FinalCTA } from './components/FinalCTA'
import { WebGLFallback } from './components/WebGLFallback'
import { usePointerInput } from './hooks/usePointerInput'
import { useQualityProfile } from './hooks/useQualityProfile'
import { useReducedMotion } from './hooks/useReducedMotion'
import { useScrollProgress } from './hooks/useScrollProgress'
import { SCENES } from './lib/content'
import { supportsWebGL } from './lib/webgl'
import type { QualityProfile } from './lib/config'

const Experience = lazy(() => import('./experience/Experience').then((module) => ({ default: module.Experience })))
const downgrade: Record<QualityProfile, QualityProfile> = { HIGH: 'MEDIUM', MEDIUM: 'LOW', LOW: 'LOW', MOBILE: 'MOBILE' }

const steps = [
  ['01', 'Déployer', 'Un premier agent prend en charge une tâche réelle sur votre infrastructure.'],
  ['02', 'Connecter', 'Il rejoint vos outils, vos données et les règles qui structurent votre activité.'],
  ['03', 'Valider', 'Les décisions sensibles convergent vers vous au lieu de disparaître dans une boîte noire.'],
  ['04', 'Opérer', 'Supervision, documentation et évolution maintiennent le système utile dans la durée.'],
]

export default function App() {
  const reducedMotion = useReducedMotion()
  const { profile, setProfile } = useQualityProfile()
  const { progressRef, hasScrolled } = useScrollProgress(SCENES.length)
  const pointerRef = usePointerInput(!reducedMotion && profile !== 'MOBILE')
  const [selectedStation, setSelectedStation] = useState(0)
  const webglAvailable = useMemo(() => supportsWebGL(), [])

  useEffect(() => {
    const elements = Array.from(document.querySelectorAll<HTMLElement>('[data-reveal]'))
    if (reducedMotion) { elements.forEach((element) => element.classList.add('is-visible')); return }
    const observer = new IntersectionObserver((entries) => entries.forEach((entry) => {
      if (entry.isIntersecting) (entry.target as HTMLElement).classList.add('is-visible')
    }), { threshold: 0.12, rootMargin: '0px 0px -8% 0px' })
    elements.forEach((element) => observer.observe(element))
    return () => observer.disconnect()
  }, [reducedMotion])

  return (
    <div className="app-shell" data-quality={profile} data-reduced-motion={reducedMotion ? 'true' : 'false'}>
      <a className="skip-link" href="#top">Aller au contenu</a>
      <Navigation visible={hasScrolled} />
      <main>
        <section id="top" className="hero" aria-labelledby="hero-title">
          <div className="hero-experience-wrap">
            {webglAvailable ? (
              <Suspense fallback={null}>
                <Experience progressRef={progressRef} pointerRef={pointerRef} profile={profile} reducedMotion={reducedMotion} selectedStation={selectedStation} onQualityDecline={() => setProfile((current) => downgrade[current])} />
              </Suspense>
            ) : <WebGLFallback />}
          </div>
          <div className="hero-shade" aria-hidden="true" />
          <div className="hero-copy" data-reveal>
            <p className="technical-label">AI AGENT INFRASTRUCTURE / PRIVATE BETA</p>
            <h1 id="hero-title" aria-label="ATLAS NEXUS"><span>ATLAS</span><span>NEXUS</span></h1>
            <p className="hero-tagline">Des agents IA installés chez vous, opérés dans la durée.</p>
            <p className="hero-intro">Je déploie vos agents, je les configure sur votre infrastructure et je veille à ce qu’ils restent utiles, fiables et sous votre contrôle.</p>
            <a className="hero-cta" href="#approach">Découvrir l’approche <span aria-hidden="true">↓</span></a>
          </div>
          <div className="hero-specs" aria-label="Principes de l’offre Atlas Nexus">
            <span><small>DEPLOYMENT</small>Premier agent en 24 h</span>
            <span><small>OWNERSHIP</small>Code et données chez vous</span>
            <span><small>CONTROL</small>Validation humaine</span>
          </div>
        </section>

        <section id="approach" className="editorial-section approach-section">
          <div className="section-index" aria-hidden="true">01</div>
          <div className="editorial-heading" data-reveal>
            <p className="technical-label">APPROACH / OWN YOUR SYSTEM</p>
            <h2>Une infrastructure.<br />Pas un SaaS de plus.</h2>
          </div>
          <div className="editorial-copy" data-reveal>
            <p className="lead">L’intelligence est installée là où votre activité existe déjà.</p>
            <p>Sur votre machine ou un VPS, les agents travaillent avec vos outils, vos règles et vos étapes de validation. Vous gardez le code, la documentation et la capacité de reprendre la main.</p>
            <a href="https://atlasnexus.tech/ia-agentique/">Voir l’offre actuelle <span>↗</span></a>
          </div>
          <div className="principle-rows" data-reveal>
            <div><span>01</span><strong>Installé chez vous</strong><p>Pas de dépendance à une plateforme propriétaire.</p></div>
            <div><span>02</span><strong>Relié au travail réel</strong><p>Mails, relances, rapports et opérations quotidiennes.</p></div>
            <div><span>03</span><strong>Conçu pour durer</strong><p>Supervision et évolution, pas une démonstration abandonnée.</p></div>
          </div>
        </section>

        <section id="method" className="method-section">
          <div className="method-intro" data-reveal>
            <p className="technical-label">METHOD / FROM TASK TO SYSTEM</p>
            <h2>Déployer. Connecter.<br />Valider. Opérer.</h2>
            <p>Une progression simple, sans transformer votre entreprise en laboratoire.</p>
          </div>
          <ol className="method-steps">
            {steps.map(([number, title, description]) => <li key={number} data-reveal><span>{number}</span><h3>{title}</h3><p>{description}</p></li>)}
          </ol>
        </section>

        <UseCaseSystems selected={selectedStation} onSelect={setSelectedStation} />

        <section className="control-section" aria-labelledby="control-title">
          <div className="control-orbit" aria-hidden="true"><i /><i /><i /></div>
          <div data-reveal>
            <p className="technical-label">CONTROL / HUMAN IN THE LOOP</p>
            <h2 id="control-title">L’IA prépare et exécute.<br />Vous gardez le dernier mot.</h2>
            <p>Les agents accélèrent le travail sans rendre les décisions opaques. Les points sensibles vous reviennent avec le contexte nécessaire.</p>
          </div>
          <ul data-reveal>
            <li><span>01</span>Sorties lisibles et vérifiables</li>
            <li><span>02</span>Étapes de validation explicites</li>
            <li><span>03</span>Documentation et formats ouverts</li>
          </ul>
        </section>

        <FinalCTA />
      </main>
      <footer className="beta-footer"><span>© 2026 Atlas Nexus</span><span>Immersive beta · noindex</span><a href="https://atlasnexus.tech/">Site principal</a></footer>
    </div>
  )
}
