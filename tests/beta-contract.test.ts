import { describe, expect, it } from 'vitest'
import { readFileSync } from 'node:fs'
import { QUALITY_SETTINGS } from '../src/lib/config'
import { PRIMARY_CTA, SCENES, USE_CASES } from '../src/lib/content'

describe('beta contract', () => {
  it('keeps the cinematic sequence complete and ordered', () => {
    expect(SCENES.map((scene) => scene.id)).toEqual(['core', 'deploy', 'automate', 'control', 'systems', 'contact'])
  })

  it('uses only real Atlas Nexus use cases and the production diagnostic CTA', () => {
    expect(USE_CASES.map((item) => item.id)).toEqual(['automation', 'reporting', 'agents', 'infrastructure', 'orchestration'])
    expect(PRIMARY_CTA.href).toBe('https://atlasnexus.tech/#contact')
  })

  it('reduces GPU load across quality tiers', () => {
    expect(QUALITY_SETTINGS.HIGH.particles).toBeGreaterThan(QUALITY_SETTINGS.MEDIUM.particles)
    expect(QUALITY_SETTINGS.MEDIUM.particles).toBeGreaterThan(QUALITY_SETTINGS.LOW.particles)
    expect(QUALITY_SETTINGS.LOW.particles).toBeGreaterThan(QUALITY_SETTINGS.MOBILE.particles)
    expect(QUALITY_SETTINGS.MOBILE.maxDpr).toBeLessThanOrEqual(1)
  })

  it('isolates the beta domain and prevents indexing', () => {
    const html = readFileSync('index.html', 'utf8')
    const cname = readFileSync('public/CNAME', 'utf8').trim()
    expect(cname).toBe('beta.atlasnexus.tech')
    expect(html).toContain('content="noindex, nofollow, noarchive"')
    expect(html).toContain('href="https://beta.atlasnexus.tech/"')
  })
})
