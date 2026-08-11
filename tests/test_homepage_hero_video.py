from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FR = (ROOT / "index.html").read_text(encoding="utf-8")
EN = (ROOT / "en" / "index.html").read_text(encoding="utf-8")
V2_CSS = (ROOT / "css" / "v2.css").read_text(encoding="utf-8")


def test_homepages_no_longer_include_the_brand_motion_video():
    for html in (FR, EN):
        assert "brand-motion-showcase" not in html
        assert "brand-motion-video" not in html
        assert "atlasnexus-hero-logo" not in html
        assert "atlasnexus-hero-poster" not in html
        assert "syncHeroVideo" not in html
        assert 'href="/css/v2.css?v=7"' in html


def test_brand_motion_assets_and_styles_are_removed():
    for relative_path in (
        "assets/atlasnexus-hero-logo.mp4",
        "assets/atlasnexus-hero-logo.webm",
        "assets/atlasnexus-hero-poster.webp",
    ):
        assert not (ROOT / relative_path).exists()
    assert ".brand-motion-" not in V2_CSS
    assert ".hero-bg-video" not in V2_CSS
