from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]

INCLUDED_ROUTES = (
    "", "agent-identity", "agent-identity/en", "ai-studio", "artisan-demo",
    "artisan-ia", "atlas-desk", "atlas-desk/en", "atlas-studio",
    "audit-responsive-pagespeed", "audit-responsive-pagespeed/en",
    "bento-beta-bounty", "cahier-presence-stagiaires", "case-study",
    "case-study/en", "cgv", "control-room", "datatoolkit",
    "demos-web", "demos-web/en", "developpement-web-donnees", "en",
    "extracteur-donnees-publiques", "framer-motion-ui", "growth",
    "ia-agentique", "ia-agentique/en", "ia-receptionniste", "install",
    "labs", "labs/en", "labs/atlas", "labs/atlas/en",
    "markets-dashboard", "mentions-legales", "merci", "oobe-ace-agent", "rendez-vous",
    "oobe-ace-agent-en", "revue-trimestrielle-powerpoint", "template-artisan",
    "training", "training/en", "verify", "verify/en",
)

EXCLUDED_ROUTES = (
    "archive", "artisan-metallier", "atlas-desk/client", "augelle-deco", "az-bois", "blueline-logistics",
    "demo-menuiserie.fr", "demo-refonte-artisan", "demo-refonte-consultant",
    "demo-refonte-restaurant", "demo-refonte-sante", "demo-seydi",
    "demo-seydi-animee", "duault-anatole", "ed-maconnerie", "en/archive",
    "eponia-conseil", "hermes", "menuiserie-devarenne", "peintre-95", "prime-agent",
    "pwa-template",
    "stratea", "tad-agency", "tony-zanirato",
)


def page(route: str) -> str:
    return (ROOT / route / "index.html").read_text(encoding="utf-8") if route else (ROOT / "index.html").read_text(encoding="utf-8")


def test_header_scope_accounts_for_every_html_page():
    all_routes = {
        "" if path.parent == ROOT else path.parent.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("index.html")
    }
    assert set(INCLUDED_ROUTES).isdisjoint(EXCLUDED_ROUTES)
    assert set(INCLUDED_ROUTES) | set(EXCLUDED_ROUTES) == all_routes


def test_included_pages_share_the_canonical_atlas_header():
    for route in INCLUDED_ROUTES:
        html = page(route)
        assert html.count('data-atlas-site-header') == 1, route
        assert '<link rel="stylesheet" href="/css/atlas-header.css?v=2">' in html, route
        assert '<script src="/js/atlas-header.js?v=1" defer></script>' in html, route
        assert '<span class="atlas-site-brand-name">Atlas Nexus</span>' in html, route
        assert 'src="/atlas-logo.png?v=20260527"' in html, route
        assert 'class="atlas-site-brand"' in html, route
        assert 'href="/#contact"' in html or 'href="/en/#contact"' in html or 'href="/rendez-vous/"' in html or route == "rendez-vous", route
        assert re.search(r'<body\b[^>]*\bclass="[^"]*\batlas-unified-header\b', html), route
        assert '<a href="https://github.com/AtlasNexusTech" target="_blank" rel="noopener noreferrer">GitHub</a>' in html, route
        assert '<button id="atlas-theme-toggle" class="atlas-theme-toggle" type="button"' in html, route
        assert 'aria-pressed="false"' in html, route
        # La navigation legacy a été supprimée (audit 13/08) : plus aucun menu masqué en production.
        assert 'data-atlas-legacy-nav' not in html, route


def test_localized_header_copy_and_language_state():
    for route in INCLUDED_ROUTES:
        html = page(route)
        lang_match = re.search(r'<html\b[^>]*\blang="([^"]+)"', html, re.I)
        is_english = bool(lang_match and lang_match.group(1).lower().startswith("en"))
        header = re.search(r'<header\b[^>]*data-atlas-site-header.*?</header>', html, re.I | re.S)
        assert header, route
        markup = header.group(0)
        if is_english:
            assert 'data-active="en"' in markup, route
            assert '>Work</a>' in markup and '>Offers</a>' in markup and '>Why</a>' in markup, route
            contact_target = "/#contact" if route == "en" else "/en/#contact"
            assert f'href="{contact_target}"' in markup, route
            fr_target = "/atlas-desk/" if route == "atlas-desk/en" else "/"
            en_target = "/atlas-desk/en/" if route == "atlas-desk/en" else "/en/"
            assert f'<a href="{fr_target}" data-atlas-lang="fr">FR</a>' in markup, route
            assert f'<a href="{en_target}" data-atlas-lang="en" aria-current="page">EN</a>' in markup, route
        else:
            assert 'data-active="fr"' in markup, route
            assert '>Réalisations</a>' in markup and '>Offres</a>' in markup and '>Pourquoi</a>' in markup, route
            assert 'href="/#contact"' in markup or 'href="/rendez-vous/"' in markup or route == "rendez-vous", route
            fr_target = "/atlas-desk/" if route == "atlas-desk" else "/"
            en_target = "/atlas-desk/en/" if route == "atlas-desk" else "/en/"
            assert f'<a href="{fr_target}" data-atlas-lang="fr" aria-current="page">FR</a>' in markup, route
            assert f'<a href="{en_target}" data-atlas-lang="en">EN</a>' in markup, route


def test_independent_prototypes_keep_their_own_headers():
    archived_routes = {"archive", "en/archive"}
    for route in EXCLUDED_ROUTES:
        html = page(route)
        if route in archived_routes:
            assert 'href="/archive/css/atlas-header.css?v=1"' in html, route
            assert 'href="/css/atlas-header.css' not in html, route
            continue
        assert 'data-atlas-site-header' not in html, route
        assert '/css/atlas-header.css' not in html, route
        assert '/js/atlas-header.js' not in html, route


def test_shared_header_assets_preserve_mobile_focus_and_theme_accessibility():
    css = (ROOT / "css" / "atlas-header.css").read_text(encoding="utf-8")
    js = (ROOT / "js" / "atlas-header.js").read_text(encoding="utf-8")
    assert ".atlas-site-brand-name" in css and "display: inline-flex" in css
    assert "@media (max-width: 640px)" in css
    assert ":focus-visible" in css
    assert "prefers-reduced-motion: reduce" in css
    assert "data-atlas-legacy-nav" not in css
    assert "atlas-theme-toggle" in js
    assert "safeStorage.set('theme'" in js
    assert "aria-pressed" in js
    assert "try {" in js and "catch (_)" in js
    for forbidden in ("fetch(", "XMLHttpRequest", "WebSocket", ".innerHTML", "insertAdjacentHTML", "eval(", "new Function"):
        assert forbidden not in js


def test_versioned_browser_contract_covers_runtime_requirements():
    browser_test = (ROOT / "tests" / "browser_verify_site_headers.py").read_text(encoding="utf-8")
    for requirement in (
        'VIEWPORTS = {', '"width": 1280', '"width": 320',
        'java_script_enabled=False', 'Storage.prototype.getItem',
        'page.keyboard.press("Tab")', 'outlineStyle', 'transitionDuration',
        'header overflow', 'aria-pressed', 'EXCLUDED',
    ):
        assert requirement in browser_test
