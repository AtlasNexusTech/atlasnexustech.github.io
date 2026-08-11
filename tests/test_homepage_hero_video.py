import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FR = (ROOT / "index.html").read_text(encoding="utf-8")
EN = (ROOT / "en" / "index.html").read_text(encoding="utf-8")
V2_CSS = (ROOT / "css" / "v2.css").read_text(encoding="utf-8")
VIDEO = ROOT / "assets" / "atlasnexus-hero-logo.mp4"
WEBM_VIDEO = ROOT / "assets" / "atlasnexus-hero-logo.webm"
POSTER = ROOT / "assets" / "atlasnexus-hero-poster.webp"


def test_homepages_show_the_video_once_in_a_native_size_panel_after_the_hero():
    for html in (FR, EN):
        hero = re.search(r'<!-- Hero -->(.*?)<!-- AvantApres -->', html, re.DOTALL)
        assert hero
        assert '<div class="hero-bg" aria-hidden="true"><img' in hero.group(1)
        assert '<video' not in re.search(r'<div class="hero-bg".*?</div>', hero.group(1), re.DOTALL).group(0)

        showcase = re.search(r'<div class="brand-motion-showcase"[^>]*>(.*?)</div>', hero.group(1), re.DOTALL)
        assert showcase, "The supplied video must be contained after the hero, not layered over its image"
        match = re.search(r'<video\b(?P<attrs>[^>]*)>.*?</video>', showcase.group(1), re.DOTALL)
        assert match
        attrs = match.group("attrs")
        for boolean_attr in ("autoplay", "muted", "playsinline"):
            assert re.search(rf"\b{boolean_attr}\b", attrs)
        assert not re.search(r"\bloop\b", attrs)
        assert 'class="brand-motion-video"' in attrs
        assert 'aria-hidden="true"' in attrs
        assert 'tabindex="-1"' in attrs
        assert 'poster="/assets/atlasnexus-hero-poster.webp"' in attrs
        assert '<source src="/assets/atlasnexus-hero-logo.webm" type="video/webm">' in match.group(0)
        assert '<source src="/assets/atlasnexus-hero-logo.mp4" type="video/mp4">' in match.group(0)
        assert "controls" not in attrs
        assert 'href="/css/v2.css?v=6"' in html
        assert "heroVideo.pause()" in html
        assert "motionPreference.addEventListener('change', syncHeroVideo)" in html


def test_video_panel_never_upscales_the_848_pixel_source():
    shell = re.search(r"\.brand-motion-shell\s*\{(?P<body>[^}]*)\}", V2_CSS, re.DOTALL)
    video_rules = re.findall(r"\.brand-motion-video\s*\{(?P<body>[^}]*)\}", V2_CSS, re.DOTALL)
    assert shell and re.search(r"max-width:\s*848px", shell.group("body"))
    assert any(re.search(r"object-fit:\s*contain", rule) for rule in video_rules)


def test_hero_video_asset_and_reduced_motion_fallback_exist():
    assert VIDEO.is_file()
    assert 100_000 < VIDEO.stat().st_size < 3_000_000
    assert WEBM_VIDEO.is_file()
    assert 100_000 < WEBM_VIDEO.stat().st_size < 2_000_000
    assert POSTER.is_file()
    reduced_motion = re.search(
        r"@media\s*\(prefers-reduced-motion:\s*reduce\)\s*\{(?P<body>.*?)\}",
        V2_CSS,
        re.DOTALL,
    )
    assert reduced_motion
    assert re.search(r"\.brand-motion-video\s*\{[^}]*display:\s*none", reduced_motion.group("body"), re.DOTALL)
