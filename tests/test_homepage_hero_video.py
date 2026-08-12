import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FR = (ROOT / "index.html").read_text(encoding="utf-8")
EN = (ROOT / "en" / "index.html").read_text(encoding="utf-8")
V2_CSS = (ROOT / "css" / "v2.css").read_text(encoding="utf-8")
MP4 = ROOT / "assets" / "atlasnexus-hero-20260812.mp4"
WEBM = ROOT / "assets" / "atlasnexus-hero-20260812.webm"
POSTER = ROOT / "assets" / "atlasnexus-hero-20260812.webp"


def test_homepages_replace_the_hero_image_with_accessible_decorative_video():
    for html in (FR, EN):
        hero = re.search(r'<!-- Hero -->(.*?)<!-- AvantApres -->', html, re.DOTALL)
        assert hero
        background = re.search(r'<div class="hero-bg".*?</div>', hero.group(1), re.DOTALL)
        assert background
        markup = background.group(0)
        video = re.search(r'<video\b(?P<attrs>[^>]*)>.*?</video>', markup, re.DOTALL)
        assert video
        attrs = video.group("attrs")
        for attr in ("autoplay", "muted", "loop", "playsinline"):
            assert re.search(rf"\b{attr}\b", attrs)
        assert 'class="hero-bg-video"' in attrs
        assert 'poster="/assets/atlasnexus-hero-20260812.webp"' in attrs
        assert 'aria-hidden="true"' in attrs
        assert 'tabindex="-1"' in attrs
        assert "controls" not in attrs
        assert '<source src="/assets/atlasnexus-hero-20260812.webm" type="video/webm">' in markup
        assert '<source src="/assets/atlasnexus-hero-20260812.mp4" type="video/mp4">' in markup
        assert '<img src="/assets/atlasnexusfond.jpg"' in markup
        assert 'href="/css/v2.css?v=8"' in html
        assert "heroVideo.pause()" in html
        assert "motionPreference.addEventListener('change', syncHeroVideo)" in html


def test_video_assets_and_responsive_non_pixelated_rendering_contract_exist():
    for asset in (MP4, WEBM):
        assert asset.is_file()
        assert asset.stat().st_size > 50_000
    assert POSTER.is_file()
    assert POSTER.stat().st_size > 10_000

    shared_media = re.search(
        r"\.hero-bg img,\s*\.hero-bg-video\s*\{(?P<body>[^}]*)\}", V2_CSS, re.DOTALL
    )
    assert shared_media
    body = shared_media.group("body")
    assert re.search(r"object-fit:\s*cover", body)
    assert re.search(r"object-position:\s*center center", body)
    assert re.search(r"\.hero-bg-video\s*\{[^}]*opacity:\s*1", V2_CSS, re.DOTALL)

    reduced_motion = re.search(
        r"@media\s*\(prefers-reduced-motion:\s*reduce\)\s*\{(?P<body>.*?)\}",
        V2_CSS,
        re.DOTALL,
    )
    assert reduced_motion
    assert re.search(r"\.hero-bg-video\s*\{[^}]*display:\s*none", reduced_motion.group("body"), re.DOTALL)
    assert re.search(r"@media\s*\(max-width:\s*900px\).*?\.hero-bg-video[^}]*object-position:\s*68% center", V2_CSS, re.DOTALL)


def test_video_assets_use_a_smooth_forward_reverse_boomerang_loop():
    for asset in (MP4, WEBM):
        probe = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration:stream=nb_frames,r_frame_rate",
                "-of",
                "json",
                str(asset),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        data = json.loads(probe.stdout)
        duration = float(data["format"]["duration"])
        assert 19.70 <= duration <= 19.75
        assert data["streams"][0]["r_frame_rate"] == "30/1"
        if asset.suffix == ".mp4":
            assert int(data["streams"][0]["nb_frames"]) == 592
