import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FR = (ROOT / "index.html").read_text(encoding="utf-8")
EN = (ROOT / "en" / "index.html").read_text(encoding="utf-8")
TRAINING_FR = (ROOT / "training" / "index.html").read_text(encoding="utf-8")
TRAINING_EN = (ROOT / "training" / "en" / "index.html").read_text(encoding="utf-8")
DEMOS_EN = (ROOT / "demos-web" / "en" / "index.html").read_text(encoding="utf-8")
LABS_EN = (ROOT / "labs" / "en" / "index.html").read_text(encoding="utf-8")
V2_CSS = (ROOT / "css" / "v2.css").read_text(encoding="utf-8")


def test_work_section_is_presented_as_work_and_demos_not_case_studies():
    assert "Réalisations" in FR
    assert "Work" in EN
    assert "Mini études de cas" not in FR
    assert "Mini case studies" not in EN


def test_homepage_service_voice_is_first_person_singular():
    # Hero actuel (refonte) : « Je vous aide à faire travailler l'Intelligence pour vous »
    assert "Je vous aide à faire travailler l'Intelligence" in FR
    assert "I help you put Intelligence to work for you" in EN
    assert "Voir comment on y va" in FR
    assert "See how we get there" in EN
    assert not re.search(r"\b(?:nous|notre|nos)\b", FR, re.IGNORECASE)
    assert "Parlons" not in FR
    assert "Let's" not in EN


def test_coaching_calls_to_action_use_stable_contact_routes():
    assert 'href="/rendez-vous/"' in FR
    assert 'href="#contact"' in EN
    for html in (FR, EN, TRAINING_FR, TRAINING_EN, DEMOS_EN):
        assert "/cdn-cgi/l/email-protection" not in html
        assert "data-cfemail" not in html
    assert "mailto:" not in TRAINING_FR
    assert "mailto:" not in TRAINING_EN
    assert "mailto:" not in DEMOS_EN
    assert 'href="/#contact"' in TRAINING_FR
    assert 'href="/en/#contact"' in TRAINING_EN
    assert "Parler à un coach" not in TRAINING_FR
    assert ">Parlez-moi</a>" in TRAINING_FR
    assert ">Talk to me</a>" in TRAINING_EN
    # La refonte a transformé le coaching en carte d'offre (150€) : « Coaching + multi-agent ecosystem »
    assert "Coaching + multi-agent ecosystem" in EN
    assert "Coaching IA" in FR


def test_english_homepage_never_routes_these_cards_to_french_pages():
    assert EN.count('href="/demos-web/en/"') >= 2
    assert 'href="/demos-web/"' not in EN
    assert 'href="/framer-motion-ui/"' in EN
    assert 'href="/training/en/"' in EN
    assert 'href="/training/"' not in EN


def test_linked_english_pages_keep_users_in_english():
    # Le header partagé contient le switch FR légitime (href="/") — contrôler
    # le CORPS de la page (après </header>), pas le header partagé.
    def body_only(html: str) -> str:
        m = re.search(r"</header>", html, re.I)
        return html[m.end():] if m else html

    for html in (TRAINING_EN, DEMOS_EN, LABS_EN):
        body = body_only(html)
        assert 'href="/"' not in body
        assert 'href="/#' not in body
        assert 'href="/framer-motion-ui/"' not in body
        assert 'href="/datatoolkit/"' not in body
    assert 'href="https://github.com/AtlasNexusTech/framer-motion-ui"' in DEMOS_EN
    assert 'href="https://github.com/AtlasNexusTech/framer-motion-ui"' in LABS_EN
    assert 'href="https://github.com/AtlasNexusTech/datatoolkit"' in LABS_EN
    assert not re.search(r"\b(?:we|our)\b", LABS_EN, re.IGNORECASE)
    assert "Let's" not in LABS_EN
    for html in (EN, DEMOS_EN, LABS_EN):
        for repo in ("framer-motion-ui", "datatoolkit"):
            if f'AtlasNexusTech/{repo}' in html:
                assert re.search(
                    rf'href="https://github\.com/AtlasNexusTech/{repo}"[^>]*'
                    r'target="_blank"[^>]*rel="[^"]*noopener[^"]*"',
                    html,
                )


def test_homepage_keeps_the_mouse_reactive_antigravity_canvas():
    for html in (FR, EN):
        assert html.count('id="antigravity-canvas"') == 1
        assert "Antigravity Canvas" in html
    assert re.search(
        r"#antigravity-canvas\s*\{[^}]*z-index:\s*2\s*!important",
        V2_CSS,
        re.DOTALL,
    )


def test_result_and_proof_panels_match_the_featured_offer_gradient():
    featured_gradient = "linear-gradient(135deg, #226CF3, #5BA2FC)"
    root_rule = re.search(r":root\s*\{([^}]+)\}", V2_CSS, re.DOTALL)
    assert root_rule
    assert f"--atlas-logo-panel: {featured_gradient}" in root_rule.group(1)

    offer_rule = re.search(r"\.offer-badge\s*\{([^}]+)\}", V2_CSS, re.DOTALL)
    assert offer_rule
    assert featured_gradient in offer_rule.group(1)

    for selector in (".ba-result", ".proof-head"):
        rule = re.search(rf"{re.escape(selector)}\s*\{{([^}}]+)\}}", V2_CSS, re.DOTALL)
        assert rule, f"Missing CSS rule for {selector}"
        assert "background: var(--atlas-logo-panel)" in rule.group(1)
