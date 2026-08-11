import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOTION_CSS = ROOT / "demo-seydi-animee" / "motion.css"


def css_rule(css: str, selector: str) -> str:
    match = re.search(
        re.escape(selector) + r"\s*\{(?P<body>.*?)\}",
        css,
        flags=re.DOTALL,
    )
    assert match, f"Règle CSS introuvable : {selector}"
    return match.group("body").lower()


def test_animated_facts_use_text_color_without_a_background():
    css = MOTION_CSS.read_text(encoding="utf-8")
    rule = css_rule(css, ".motion-page .facts strong")

    assert "background" not in rule
    assert "transparent" not in rule
    assert "--fact-color-start" in rule
    assert "--fact-color-end" in rule
    assert "background-clip: text" not in css
    assert "text-fill-color: transparent" not in css


def test_dark_property_fact_animation_finishes_in_gold():
    css = MOTION_CSS.read_text(encoding="utf-8")
    rule = css_rule(css, ".motion-page .property-dark .facts strong")
    keyframes = css.split("@keyframes number-shine", 1)[1].split(
        "@keyframes monogram-pulse", 1
    )[0].lower()

    assert "background" not in rule
    assert "--fact-color-start: #f4deb0" in rule
    assert "--fact-color-mid: #d6ad62" in rule
    assert "--fact-color-end: #bd9b5d" in rule
    assert "color: var(--fact-color-end)" in keyframes


def test_reduced_motion_displays_final_fact_color_directly():
    css = MOTION_CSS.read_text(encoding="utf-8")
    reduced_motion = css.split("@media (prefers-reduced-motion: reduce)", 1)[1]
    rule = css_rule(reduced_motion, ".motion-page .facts strong")

    assert "color: var(--fact-color-end)" in rule
    assert "background" not in rule
    assert "animation: none" in rule
