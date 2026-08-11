import { expect, test } from '@playwright/test'

const viewports = [
  { name: 'mobile-375', width: 375, height: 812 },
  { name: 'mobile-430', width: 430, height: 932 },
  { name: 'tablet-768', width: 768, height: 1024 },
  { name: 'landscape-1024', width: 1024, height: 768 },
  { name: 'desktop-1440', width: 1440, height: 900 },
  { name: 'desktop-1920', width: 1920, height: 1080 },
  { name: 'ultrawide-2560', width: 2560, height: 1080 },
]

for (const viewport of viewports) {
  test(`${viewport.name}: content, WebGL and layout`, async ({ page }) => {
    const errors: string[] = []
    page.on('console', (message) => {
      if (message.type() === 'error') errors.push(message.text())
    })
    page.on('pageerror', (error) => errors.push(error.message))
    await page.setViewportSize(viewport)
    await page.goto('/', { waitUntil: 'networkidle' })
    await expect(page.getByRole('heading', { name: 'ATLAS NEXUS' })).toBeVisible()
    await expect(page.locator('canvas')).toHaveCount(1)
    await expect(page.locator('meta[name="robots"]')).toHaveAttribute('content', 'noindex, nofollow, noarchive')
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth)
    expect(overflow).toBeLessThanOrEqual(1)
    await page.locator('#systems').scrollIntoViewIfNeeded()
    await expect(page.getByRole('heading', { name: 'Des capacités reliées à votre activité.' })).toBeVisible()
    await page.getByRole('tab', { name: /infrastructure/i }).click()
    await expect(page.getByRole('heading', { name: 'Garder les agents là où vous les maîtrisez.' })).toBeVisible()
    expect(errors).toEqual([])
  })
}

test('reduced motion preserves all essential content', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' })
  await page.setViewportSize({ width: 430, height: 932 })
  await page.goto('/', { waitUntil: 'networkidle' })
  await expect(page.locator('.app-shell')).toHaveAttribute('data-reduced-motion', 'true')
  await page.locator('#contact').scrollIntoViewIfNeeded()
  await expect(page.getByRole('link', { name: /Réserver mon diagnostic gratuit/i })).toBeVisible()
})

test('the beta ships a dedicated branded 404 document', async ({ page }) => {
  const response = await page.goto('/404.html')
  expect(response?.status()).toBe(200)
  await expect(page.getByRole('heading', { name: 'Signal introuvable.' })).toBeVisible()
})
