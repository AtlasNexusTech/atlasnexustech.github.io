from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = (ROOT / "index.html").read_text(encoding="utf-8")
HERMES = (ROOT / "hermes" / "index.html").read_text(encoding="utf-8")
MOTION = (ROOT / "hermes" / "motion.css").read_text(encoding="utf-8")
PRIME = (ROOT / "prime-agent" / "index.html").read_text(encoding="utf-8")
PRIME_MOTION = (ROOT / "prime-agent" / "motion.css").read_text(encoding="utf-8")
PRIME_MOTION_JS = (ROOT / "prime-agent" / "motion.js").read_text(encoding="utf-8")


def test_homepage_links_to_hermes_and_prime_agent():
    assert 'href="/hermes/"' in HOME
    assert 'href="/prime-agent/"' in HOME
    assert 'src="/assets/hermes-portrait.jpg"' in HOME
    assert 'src="/assets/prime-agent-identity.jpg"' in HOME
    assert 'class="work-shot work-hermes-shot"' not in HOME
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


def test_prime_agent_is_a_real_installation_page_not_a_dead_redirect():
    assert '<title>Installation Prime-Agent — Atlas Nexus</title>' in PRIME
    assert 'Demander l’installation' in PRIME
    assert 'http-equiv="refresh"' not in PRIME
    assert 'location.replace' not in PRIME
    assert 'Claude Opus 5' in PRIME
    assert 'OAuth Anthropic' in PRIME
    assert 'Raisonnement configurable jusqu’à <strong>max</strong>' in PRIME
    assert 'Noyau IPython' in PRIME
    assert 'Sessions reprenables, forkables et sous-agents' in PRIME
    assert 'Mode autonome avec critères de validation' in PRIME
    assert 'href="#method">Installation</a>' not in PRIME
    assert 'class="button button-small nav-cta"' not in PRIME


def test_prime_agent_motion_is_choreographed_and_accessible():
    assert 'href="/prime-agent/motion.css"' in PRIME
    assert 'src="/prime-agent/motion.js"' in PRIME
    assert 'PRIME AGENT MOTION STORYBOARD' in PRIME_MOTION_JS
    assert 'const TIMING = Object.freeze' in PRIME_MOTION_JS
    assert 'prefers-reduced-motion:reduce' in PRIME_MOTION
    assert 'animation:none!important' in PRIME_MOTION
    assert '.prime-page .site-header .brand>span{display:none}' in PRIME_MOTION


def test_new_assets_exist():
    for relative in (
        "assets/hermes-portrait.jpg",
        "assets/prime-agent-identity.jpg",
        "css/home-solutions.css",
        "hermes/styles.css",
        "hermes/motion.css",
        "hermes/app.js",
        "prime-agent/prime.css",
        "prime-agent/edge.css",
        "prime-agent/motion.css",
        "prime-agent/motion.js",
    ):
        assert (ROOT / relative).is_file(), relative
