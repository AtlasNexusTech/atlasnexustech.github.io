from pathlib import Path
from playwright.sync_api import sync_playwright
import os

BASE = os.environ.get("ATLAS_QA_BASE", "http://127.0.0.1:4174")
OUT = Path(__file__).resolve().parents[1] / "qa"
OUT.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    failures = []
    for name, width, height in [("desktop", 1440, 1000), ("mobile", 390, 844)]:
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
        console_errors = []
        failed_requests = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("requestfailed", lambda req: failed_requests.append(f"{req.url}: {req.failure}"))

        page.goto(BASE + "/", wait_until="networkidle")
        home_metrics = page.evaluate("""() => ({
          viewport: innerWidth,
          documentWidth: document.documentElement.scrollWidth,
          hermesLinks: document.querySelectorAll('a[href="/hermes/"]').length,
          primeLinks: document.querySelectorAll('a[href="/prime-agent/"]').length,
          imageReady: !!document.querySelector('.agent-solution-hermes-visual img')?.complete,
          primeLogoReady: !!document.querySelector('.agent-solution-prime-visual img')?.complete
        })""")
        if home_metrics["documentWidth"] > home_metrics["viewport"] + 1:
            failures.append(f"home {name}: horizontal overflow {home_metrics}")
        if home_metrics["hermesLinks"] < 1 or home_metrics["primeLinks"] < 1 or not home_metrics["imageReady"] or not home_metrics["primeLogoReady"]:
            failures.append(f"home {name}: links/image {home_metrics}")
        page.locator("#solutions-agentiques").scroll_into_view_if_needed()
        page.wait_for_timeout(450)
        page.locator("#solutions-agentiques").screenshot(path=str(OUT / f"home-solutions-{name}.png"))
        page.locator("#work").scroll_into_view_if_needed()
        page.wait_for_timeout(450)
        page.locator("#work").screenshot(path=str(OUT / f"home-work-{name}.png"))

        page.goto(BASE + "/hermes/", wait_until="networkidle")
        page.wait_for_timeout(550)
        hermes_metrics = page.evaluate("""() => ({
          viewport: innerWidth,
          documentWidth: document.documentElement.scrollWidth,
          title: document.title,
          canonical: document.querySelector('link[rel="canonical"]')?.href,
          motion: !!document.querySelector('.demo-progress') && !!document.querySelector('.demo-signal'),
          reducedRule: [...document.styleSheets].some(s => { try { return [...s.cssRules].some(r => r.media?.mediaText?.includes('prefers-reduced-motion')); } catch(e) { return false; } })
        })""")
        if hermes_metrics["documentWidth"] > hermes_metrics["viewport"] + 1:
            failures.append(f"hermes {name}: horizontal overflow {hermes_metrics}")
        if not hermes_metrics["motion"] or not hermes_metrics["reducedRule"]:
            failures.append(f"hermes {name}: motion contract {hermes_metrics}")
        page.screenshot(path=str(OUT / f"hermes-hero-{name}.png"), full_page=False)

        page.goto(BASE + "/prime-agent/", wait_until="networkidle")
        page.wait_for_timeout(400)
        prime_metrics = page.evaluate("""() => ({
          viewport: innerWidth,
          documentWidth: document.documentElement.scrollWidth,
          title: document.title,
          h1: document.querySelector('h1')?.innerText,
          canonical: document.querySelector('link[rel="canonical"]')?.href,
          hasRedirect: !!document.querySelector('meta[http-equiv="refresh"]')
        })""")
        if prime_metrics["documentWidth"] > prime_metrics["viewport"] + 1 or prime_metrics["hasRedirect"]:
            failures.append(f"prime {name}: route contract {prime_metrics}")
        page.screenshot(path=str(OUT / f"prime-hero-{name}.png"), full_page=False)
        edge = page.locator("#difference")
        edge.scroll_into_view_if_needed()
        page.wait_for_timeout(350)
        if "Claude Opus 5" not in edge.inner_text() or "OAuth Anthropic" not in edge.inner_text():
            failures.append(f"prime {name}: competitive claims missing")
        page.evaluate("document.querySelector('#difference').scrollIntoView({block:'start'})")
        page.wait_for_timeout(850)
        page.screenshot(path=str(OUT / f"prime-edge-{name}.png"), full_page=False)
        if console_errors:
            failures.append(f"{name} console: {console_errors}")
        if failed_requests:
            failures.append(f"{name} requests: {failed_requests}")
        page.close()
    browser.close()

if failures:
    raise SystemExit("\n".join(failures))
print("PLAYWRIGHT_QA_OK")
