import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FR = (ROOT / "index.html").read_text(encoding="utf-8")
EN = (ROOT / "en" / "index.html").read_text(encoding="utf-8")
V2_CSS = (ROOT / "css" / "v2.css").read_text(encoding="utf-8")
WEBP = ROOT / "assets" / "atlasnexus-hero-20260813.webp"
JPG = ROOT / "assets" / "atlasnexus-hero-20260813.jpg"


def test_homepages_use_a_still_hero_image_instead_of_the_video():
    """Le proprietaire a remplace la video du hero (pixellisee, filigrane Gemini)
    par une image fixe fournie le 12/08/2026."""
    for html in (FR, EN):
        hero = re.search(r"<!-- Hero -->(.*?)<!-- AvantApres -->", html, re.DOTALL)
        assert hero
        background = re.search(r'<div class="hero-bg".*?</div>', hero.group(1), re.DOTALL)
        assert background
        markup = background.group(0)
        assert "<video" not in markup
        assert "atlasnexus-hero-20260812" not in markup
        assert '<source srcset="/assets/atlasnexus-hero-symbol-20260813.webp" type="image/webp">' in markup
        img = re.search(r"<img\b(?P<attrs>[^>]*)>", markup)
        assert img
        attrs = img.group("attrs")
        assert 'class="hero-bg-still"' in attrs
        assert 'src="/assets/atlasnexus-hero-symbol-20260813-hq.jpg"' in attrs
        assert 'alt=""' in attrs
        assert 'loading="eager"' in attrs
        assert 'decoding="async"' in attrs
        assert 'href="/css/v2.css?v=12"' in html


def test_no_hero_video_asset_is_referenced_or_scripted_any_more():
    for html in (FR, EN):
        assert "hero-bg-video" not in html
        assert "heroVideo" not in html
        assert "atlasnexus-hero-20260812" not in html


def test_hero_image_assets_exist_and_are_high_definition():
    for asset in (WEBP, JPG):
        assert asset.is_file()
        assert asset.stat().st_size > 40_000
    from PIL import Image

    for asset in (WEBP, JPG):
        with Image.open(asset) as image:
            width, height = image.size
        assert width == 1920
        assert height >= 1000


def test_still_hero_keeps_the_video_rendering_contract():
    assert ".hero-bg-video" not in V2_CSS   # plus aucune trace de la video
    layout = re.search(r"\.hero-bg img\s*\{(?P<body>[^}]*object-fit[^}]*)\}", V2_CSS, re.DOTALL)
    assert layout
    body = layout.group("body")
    assert re.search(r"object-fit:\s*cover", body)
    assert re.search(r"object-position:\s*center center", body)
    # pleine opacite en clair comme en sombre, contrairement a l'image de fond decorative
    assert re.search(r"\.hero-bg img\.hero-bg-still\s*\{[^}]*opacity:\s*1", V2_CSS)
    assert re.search(r"\.dark \.hero-bg img\.hero-bg-still\s*\{[^}]*opacity:\s*1", V2_CSS)
    # le mouvement reste desactivable
    reduced_motion = re.search(
        r"@media\s*\(prefers-reduced-motion:\s*reduce\)\s*\{(?P<body>.*?\})\s*\}",
        V2_CSS, re.DOTALL,
    )
    assert reduced_motion
    assert re.search(r"\.hero-bg img\s*\{[^}]*animation:\s*none", reduced_motion.group("body"), re.DOTALL)
