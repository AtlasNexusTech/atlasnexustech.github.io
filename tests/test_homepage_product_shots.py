from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
FR = (ROOT / "index.html").read_text(encoding="utf-8")
EN = (ROOT / "en" / "index.html").read_text(encoding="utf-8")
SHOTS = {
    "shot-markets.jpg": "4589104cd0f663f3c37ea151083bec1a90ef2606a4b961276e5687e17b8aeded",
    "shot-desk.jpg": "192f1b7a40135a0be846f9058e2858368b339c790ed606d32377790f60bf82c1",
}


def test_removed_homepage_product_cards_do_not_reference_stale_screenshots():
    for filename in SHOTS:
        expected_src = f'/assets/shots/{filename}?v=20260812-ui2'
        assert expected_src not in FR
        assert expected_src not in EN


def test_product_screenshots_are_crisp_card_native_images():
    for filename in SHOTS:
        with Image.open(ROOT / "assets" / "shots" / filename) as image:
            assert image.size == (1280, 800)
            assert image.mode == "RGB"
