"""Browser contract for the shared Atlas Nexus header.

Run against a local snapshot server with:
ATLAS_HEADER_BASE=http://127.0.0.1:8767 python tests/browser_verify_site_headers.py
"""

from pathlib import Path
import os
import runpy

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
DATA = runpy.run_path(str(ROOT / "tests" / "test_site_header_consistency.py"))
INCLUDED = DATA["INCLUDED_ROUTES"]
EXCLUDED = DATA["EXCLUDED_ROUTES"]
BASE = os.environ.get("ATLAS_HEADER_BASE", "http://127.0.0.1:8766").rstrip("/")
VIEWPORTS = {
    "desktop": {"width": 1280, "height": 800},
    "mobile": {"width": 320, "height": 720},
}


def url(route: str) -> str:
    suffix = f"{route}/" if route else ""
    return f"{BASE}/{suffix}?header-browser-contract=1"


def block_fonts(page) -> None:
    page.route(
        "https://fonts.googleapis.com/**",
        lambda route: route.fulfill(status=200, content_type="text/css", body=""),
    )
    page.route("https://fonts.gstatic.com/**", lambda route: route.abort())


def assert_header(page, route: str, mode: str, viewport: dict[str, int]) -> None:
    response = page.goto(url(route), wait_until="domcontentloaded", timeout=45_000)
    assert response and response.ok, (route, mode, response.status if response else None)
    page.wait_for_timeout(350)

    header = page.locator("[data-atlas-site-header]")
    assert header.count() == 1 and header.is_visible(), (route, mode, "header")
    assert header.evaluate("el => getComputedStyle(el).position") == "fixed", (route, mode, "position")
    header_box = header.bounding_box()
    assert header_box and header_box["x"] >= -1, (route, mode, header_box)
    assert header_box["x"] + header_box["width"] <= viewport["width"] + 1, (route, mode, header_box)

    logo_box = page.locator(".atlas-site-brand-logo").bounding_box()
    name = page.locator(".atlas-site-brand-name")
    name_box = name.bounding_box()
    assert name.is_visible() and name.inner_text() == "Atlas Nexus", (route, mode, "brand")
    assert logo_box and name_box and name_box["x"] >= logo_box["x"] + logo_box["width"] - 1, (
        route, mode, logo_box, name_box
    )

    assert page.locator("[data-atlas-legacy-nav]:visible").count() == 0, (route, mode, "legacy nav")
    assert page.locator(".atlas-site-language a[aria-current='page']").count() == 1, route
    assert page.locator(".atlas-site-contact").get_attribute("href") in ("/#contact", "/en/#contact"), route

    header_overflow = header.evaluate("""el => {
      const viewport = document.documentElement.clientWidth;
      return [...el.querySelectorAll('*')].some(node => {
        const rect = node.getBoundingClientRect();
        return rect.left < -1 || rect.right > viewport + 1;
      });
    }""")
    assert not header_overflow, (route, mode, "header overflow")

    page.evaluate("document.activeElement && document.activeElement.blur()")
    page.keyboard.press("Tab")
    assert page.locator(".atlas-site-brand").evaluate("el => document.activeElement === el"), (
        route, mode, "first tab stop"
    )
    assert page.locator(".atlas-site-brand").evaluate("el => getComputedStyle(el).outlineStyle") != "none", (
        route, mode, "focus visible"
    )

    assert page.locator(".atlas-site-contact").evaluate("el => getComputedStyle(el).transitionDuration") == "0s", (
        route, mode, "reduced motion"
    )


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)

    for mode, viewport in VIEWPORTS.items():
        for route in INCLUDED:
            page = browser.new_page(viewport=viewport, reduced_motion="reduce")
            block_fonts(page)
            errors = []
            page.on("pageerror", lambda error, bucket=errors: bucket.append(str(error)))
            assert_header(page, route, mode, viewport)
            assert not [error for error in errors if "atlas-header" in error.lower()], (route, mode, errors)
            page.close()

    for route in INCLUDED:
        page = browser.new_page(viewport=VIEWPORTS["desktop"])
        block_fonts(page)
        page.goto(url(route), wait_until="domcontentloaded", timeout=45_000)
        toggle = page.locator("#atlas-theme-toggle")
        before = page.locator("html").evaluate("el => el.classList.contains('dark')")
        toggle.click()
        after = page.locator("html").evaluate("el => el.classList.contains('dark')")
        assert before != after, (route, "theme")
        assert toggle.get_attribute("aria-pressed") == str(after).lower(), (route, "aria-pressed")
        page.close()

    for route in EXCLUDED:
        page = browser.new_page(viewport=VIEWPORTS["desktop"])
        response = page.goto(url(route), wait_until="domcontentloaded", timeout=45_000)
        assert response and response.ok, route
        assert page.locator("[data-atlas-site-header]").count() == 0, route
        page.close()

    for route in ("", "en", "atlas-studio", "template-artisan"):
        context = browser.new_context(viewport=VIEWPORTS["mobile"], java_script_enabled=False)
        page = context.new_page()
        response = page.goto(url(route), wait_until="domcontentloaded", timeout=45_000)
        assert response and response.ok, route
        assert page.locator("[data-atlas-site-header]").is_visible(), (route, "no JavaScript")
        assert page.locator(".atlas-site-brand-name").is_visible(), (route, "no JavaScript brand")
        context.close()

    storage_context = browser.new_context(viewport=VIEWPORTS["desktop"])
    storage_context.add_init_script("""
      Storage.prototype.getItem = () => { throw new Error('storage blocked'); };
      Storage.prototype.setItem = () => { throw new Error('storage blocked'); };
    """)
    page = storage_context.new_page()
    storage_errors = []
    page.on("pageerror", lambda error: storage_errors.append(str(error)))
    page.goto(url(""), wait_until="domcontentloaded", timeout=45_000)
    before = page.locator("html").evaluate("el => el.classList.contains('dark')")
    page.locator("#atlas-theme-toggle").click()
    after = page.locator("html").evaluate("el => el.classList.contains('dark')")
    assert before != after
    assert not [error for error in storage_errors if "atlas-header" in error.lower()], storage_errors
    storage_context.close()

    browser.close()

print(
    f"Header browser contract OK: {len(INCLUDED)} routes x 2 reduced-motion viewports, "
    f"{len(INCLUDED)} theme toggles, {len(EXCLUDED)} exclusions, 4 no-JS, blocked storage"
)
