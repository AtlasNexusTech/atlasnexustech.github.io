import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FR = (ROOT / "index.html").read_text(encoding="utf-8")
EN = (ROOT / "en" / "index.html").read_text(encoding="utf-8")
V2_CSS = (ROOT / "css" / "v2.css").read_text(encoding="utf-8")
VIDEO = ROOT / "assets" / "atlasnexus-hero-logo.mp4"
WEBM_VIDEO = ROOT / "assets" / "atlasnexus-hero-logo.webm"


def test_homepages_use_the_supplied_logo_video_as_a_safe_decorative_hero():
    for html in (FR, EN):
        match = re.search(r'<video\b(?P<attrs>[^>]*)>.*?</video>', html, re.DOTALL)
        assert match, "The homepage hero must contain the supplied logo video"
        attrs = match.group("attrs")
        for boolean_attr in ("autoplay", "muted", "loop", "playsinline"):
            assert re.search(rf"\b{boolean_attr}\b", attrs)
        assert 'class="hero-bg-video"' in attrs
        assert 'aria-hidden="true"' in attrs
        assert 'tabindex="-1"' in attrs
        assert 'poster="/assets/atlasnexusfond.jpg"' in attrs
        assert '<source src="/assets/atlasnexus-hero-logo.webm" type="video/webm">' in match.group(0)
        assert '<source src="/assets/atlasnexus-hero-logo.mp4" type="video/mp4">' in match.group(0)
        assert "controls" not in attrs
        assert 'href="/css/v2.css?v=5"' in html
        assert "heroVideo.pause()" in html
        assert "motionPreference.addEventListener('change', syncHeroVideo)" in html


def test_hero_video_asset_and_reduced_motion_fallback_exist():
    assert VIDEO.is_file()
    assert 100_000 < VIDEO.stat().st_size < 3_000_000
    assert WEBM_VIDEO.is_file()
    assert 100_000 < WEBM_VIDEO.stat().st_size < 2_000_000
    reduced_motion = re.search(
        r"@media\s*\(prefers-reduced-motion:\s*reduce\)\s*\{(?P<body>.*?)\}",
        V2_CSS,
        re.DOTALL,
    )
    assert reduced_motion
    assert re.search(r"\.hero-bg-video\s*\{[^}]*display:\s*none", reduced_motion.group("body"), re.DOTALL)
