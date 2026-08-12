import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTES = (
    "ed-maconnerie",
    "menuiserie-devarenne",
    "tony-zanirato",
    "augelle-deco",
    "az-bois",
    "peintre-95",
    "duault-anatole",
    "artisan-metallier",
)
PHONE = re.compile(r"(?:\+33|0)[1-9](?:[ .-]?\d{2}){4}")
EMAIL = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)
POSTAL_ADDRESS = re.compile(r"\b\d{1,4}\s+(?:rue|av\.|avenue|route|chemin|boulevard|impasse)\b", re.I)
LEGAL_ID = re.compile(r"\b(?:siret|siren|ape\s*:|gérant)\b", re.I)
MANAGER_IDENTITIES = re.compile(r"Eric\s+DELIN|Dominique\s+DEVARENNE|Patrick\s+Soudry", re.I)
UNSTABLE_ICONS = ("📋", "📞", "✉", "🎨", "🧱", "🪵", "🏗", "✨")


def page(route: str) -> str:
    return (ROOT / route / "index.html").read_text(encoding="utf-8")


def test_each_sector_site_is_explicitly_an_independent_demo():
    for route in ROUTES:
        html = page(route)
        assert re.search(r"<title>[^<]*Démo web", html, re.I), route
        assert re.search(
            r'<meta\s+name="description"\s+content="[^"]*Démo web indépendante',
            html,
            re.I,
        ), route
        assert '<meta name="robots" content="noindex, nofollow">' in html, route
        assert 'data-demo-notice' in html, route
        assert "Démo web indépendante" in html, route
        assert "Concept non officiel" in html, route
        assert 'href="/demos-web/"' in html, route


def test_demo_contact_surfaces_cannot_contact_or_impersonate_a_business():
    for route in ROUTES:
        html = page(route)
        lowered = html.lower()
        assert "tel:" not in lowered, route
        assert "mailto:" not in lowered, route
        assert "formspree" not in lowered, route
        assert not PHONE.search(html), route
        assert not EMAIL.search(html), route
        assert not POSTAL_ADDRESS.search(html), route
        assert not LEGAL_ID.search(html), route
        assert not MANAGER_IDENTITIES.search(html), route
        assert "Demande envoyée" not in html, route
        assert "nous vous rappel" not in html.lower(), route
        assert not any(unicodedata.category(char) == "Cf" or ord(char) >= 0x1F000 for char in html), route
        assert "ed.maconnerie.free.fr" not in html, route
        assert "google.fr/maps/place/Menuiserie" not in html, route
        assert "réactivité garantie" not in html.lower(), route
        assert "nous traitons votre demande" not in html.lower(), route
        assert "nous vous répondons rapidement" not in html.lower(), route
        form_match = re.search(r"<form\b.*?</form>", html, re.I | re.S)
        assert form_match, route
        form = form_match.group(0)
        assert re.search(r'<button\b[^>]*type="button"[^>]*data-demo-submit[^>]*>\s*Simuler l’envoi\s*</button>', form, re.I | re.S), route
        assert not re.search(r'<button\b[^>]*type="submit"', form, re.I), route
        assert "Aucune donnée n’est transmise" in form, route
        assert 'href="/#contact"' in form, route
        for select in re.findall(r'<select\b[^>]*>', form, re.I):
            assert 'aria-label="' in select, (route, select)
        assert "Créer un site similaire" in html, route
        assert not any(icon in html for icon in UNSTABLE_ICONS), route
        assert "Envoyer" not in form, route


def test_demo_pages_share_accessible_shell_and_landmarks():
    for route in ROUTES:
        html = page(route)
        assert '<link rel="stylesheet" href="/css/demo-showcase.css?v=2">' in html, route
        assert '<script src="/js/demo-showcase.js?v=2" defer></script>' in html, route
        assert re.search(r'<body\b[^>]*data-demo-palette="[^"]+"', html, re.I), route
        assert len(re.findall(r"<main\b", html, re.I)) == 1, route
        assert len(re.findall(r"</main>", html, re.I)) == 1, route
        assert re.search(r'<a\b[^>]*class="[^"]*skip-link', html, re.I), route
        assert '<main id="demo-content" tabindex="-1">' in html, route
        assert "Démo par <a" not in html, route
        ids = set(re.findall(r'\bid="([^"]+)"', html, re.I))
        for fragment in re.findall(r'href="#([^"]+)"', html, re.I):
            assert fragment in ids, (route, fragment)
        for resource in re.findall(r'(?:src|href)="([^"]+)"', html, re.I):
            assert "Coordonnées non actives" not in resource, (route, resource)
        for anchor in re.findall(r"<a\b[^>]*>", html, re.I):
            if 'target="_blank"' in anchor:
                assert re.search(r'rel="[^"]*noopener', anchor), (route, anchor)


def test_shared_demo_shell_prevents_submission_and_supports_focus():
    css = (ROOT / "css" / "demo-showcase.css").read_text(encoding="utf-8")
    js = (ROOT / "js" / "demo-showcase.js").read_text(encoding="utf-8")
    assert ".skip-link:focus" in css
    assert ":focus-visible" in css
    assert "prefers-reduced-motion" in css
    assert "animation-duration: 0.01ms !important" in css
    assert "transition-duration: 0.01ms !important" in css
    assert 'body[data-demo-palette="brick"]' in css
    assert ".bg-brand-600" in css
    assert "event.preventDefault()" in js
    assert "data-demo-submit" in js
    assert "data-demo-status" in js
    assert "aria-live" in js


def test_shared_demo_motion_is_progressive_and_respects_user_preferences():
    css = (ROOT / "css" / "demo-showcase.css").read_text(encoding="utf-8")
    js = (ROOT / "js" / "demo-showcase.js").read_text(encoding="utf-8")
    assert ".atlas-motion-ready .atlas-reveal" in css
    assert ".atlas-reveal.is-visible" in css
    assert "@keyframes atlas-hero-drift" in css
    assert "@keyframes atlas-cta-glow" in css
    assert "IntersectionObserver" in js
    assert "prefers-reduced-motion: reduce" in js
    assert "atlas-motion-ready" in js
    assert "atlas-reveal" in js
    reduced_motion = css.split("@media (prefers-reduced-motion: reduce)", 1)[1]
    assert ".atlas-reveal" in reduced_motion
    assert "opacity: 1 !important" in reduced_motion
    assert "transform: none !important" in reduced_motion


def test_shared_motion_is_the_only_guarded_intersection_observer():
    js = (ROOT / "js" / "demo-showcase.js").read_text(encoding="utf-8")
    assert js.count("new IntersectionObserver") == 1
    assert "!('IntersectionObserver' in window)" in js
    for route in ROUTES:
        html = page(route)
        assert "new IntersectionObserver" not in html, route
        assert "Gallery slide-in observer" not in html, route
