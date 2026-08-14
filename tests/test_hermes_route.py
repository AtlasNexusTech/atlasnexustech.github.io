from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = (ROOT / "index.html").read_text(encoding="utf-8")
HERMES = (ROOT / "hermes" / "index.html").read_text(encoding="utf-8")
MOTION = (ROOT / "hermes" / "motion.css").read_text(encoding="utf-8")


def test_homepage_links_to_hermes_and_prime_agent():
    assert 'href="/hermes/"' in HOME
    assert 'href="/prime-agent/"' in HOME
    assert 'src="/assets/hermes-portrait.jpg"' in HOME
    assert 'src="/assets/prime-agent-identity.jpg"' in HOME
    assert 'class="work-shot work-hermes-shot"' not in HOME
    assert '>Installation Hermes</a>' in HOME
    assert '>Installation Prime-Agent</a>' in HOME
    assert 'Découvrir Hermes' in HOME
    assert 'Découvrir Prime Agent' in HOME


def test_hermes_route_has_production_canonical_and_home_link():
    assert 'href="https://atlasnexus.tech/hermes/"' in HERMES
    assert '<title>Installation Hermes — Atlas Nexus</title>' in HERMES
    assert '<a class="brand" href="/"' in HERMES


def test_motion_is_decorative_and_accessible():
    assert 'demo-signal' in HERMES
    assert 'demo-progress' in HERMES
    assert 'prefers-reduced-motion:reduce' in MOTION
    assert 'animation:none!important' in MOTION


def test_new_assets_exist():
    for relative in (
        "assets/hermes-portrait.jpg",
        "assets/prime-agent-identity.jpg",
        "css/home-solutions.css",
        "hermes/styles.css",
        "hermes/motion.css",
        "hermes/app.js",
    ):
        assert (ROOT / relative).is_file(), relative
