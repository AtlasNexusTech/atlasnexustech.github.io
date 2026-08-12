import html as html_module
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME_STYLES = ROOT / "css" / "home.css"


def _labs_section(html: str) -> str:
    match = re.search(r'<section id="labs".*?</section>', html, re.S)
    assert match, "homepage must expose the Atlas Nexus Lab section"
    return match.group(0)


def test_lab_is_compact_automatic_marquee_in_both_locales():
    css = HOME_STYLES.read_text(encoding="utf-8")
    assert ".lab-marquee" in css
    assert "overflow: hidden" in css
    assert ".lab-track" in css
    assert "animation: lab-scroll" in css
    assert "@keyframes lab-scroll" in css
    assert ".lab-card" in css
    assert "flex: 0 0 13.5rem" in css
    assert "padding: 1rem !important" in css
    assert "animation-play-state: paused" in css
    assert ".lab-marquee.is-paused .lab-track" in css
    assert ".lab-motion-toggle" in css
    assert ".lab-step-control" in css
    assert ".lab-controls" in css
    assert ".lab-track.is-keyboard-paused { animation: none; transform: translateX(0); }" in css
    assert "prefers-reduced-motion: reduce" in css
    assert ".lab-track { width: 100%; flex-wrap: wrap; animation: none !important; }" in css

    for relative_path, secondary_copy in (
        ("index.html", "Prototypes, open source et R&D"),
        ("en/index.html", "Prototypes, open source and R&D"),
    ):
        html = (ROOT / relative_path).read_text(encoding="utf-8")
        section = _labs_section(html)
        assert 'class="lab-marquee"' in section
        assert 'class="lab-track"' in section
        assert 'class="lab-motion-toggle"' in section
        assert 'class="lab-controls"' in section
        assert len(re.findall(r'class="lab-step-control"', section)) == 2
        assert 'data-direction="-1"' in section
        assert 'data-direction="1"' in section
        assert 'aria-label=' in section
        assert 'aria-pressed="false"' in section
        assert len(re.findall(r'\blab-card\b', section)) == 5
        assert secondary_copy in html_module.unescape(section)
        assert re.search(r'<a[^>]+class="[^"]*lab-card[^"]*"', section)
        assert "cloneNode(true)" in html
        assert "aria-hidden" in html
        assert "track.addEventListener('focusin'" in html
        assert "track.addEventListener('focusout'" in html
        assert "matchMedia('(prefers-reduced-motion: reduce)')" in html
        assert "toggle.addEventListener('click'" in html
        assert "manualControls.forEach" in html
        assert "const manualQueue = []" in html
        assert "manualQueue.push" in html
        assert "animation.currentTime" in html
        assert "animation.play()" in html
        assert "cardWidth + gap" in html
        assert "motionQuery.addEventListener('change'" in html
        assert "clone.remove()" in html
        assert not re.search(r'"\s+w-\d+\s+shrink-0\s+snap-start(?:\s|>)', section)


def test_paid_offers_remain_visually_dominant_before_lab():
    for relative_path in ("index.html", "en/index.html"):
        html = (ROOT / relative_path).read_text(encoding="utf-8")
        offers_pos = html.index('<section id="offers"')
        labs_pos = html.index('<section id="labs"')
        assert offers_pos < labs_pos
        offers = html[offers_pos:labs_pos]
        assert offers.count("offer-card") == 3
        assert "p-12" in offers


def test_atlas_distributed_cognition_is_a_lab_card_not_a_framework_category():
    expectations = (
        ("index.html", "ATLAS : Cognition distribuée", "/labs/atlas/"),
        ("en/index.html", "ATLAS : Distributed Cognition", "/labs/atlas/en/"),
    )
    for relative_path, title, href in expectations:
        html = (ROOT / relative_path).read_text(encoding="utf-8")
        section = _labs_section(html)
        assert title in html_module.unescape(section)
        assert f'href="{href}"' in section
        assert '<section id="framework"' not in html
        assert not re.search(r'>\s*Framework\s*</a>', html)
