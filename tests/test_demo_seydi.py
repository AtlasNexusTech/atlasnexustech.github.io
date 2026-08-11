from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "demo-seydi" / "index.html"


class DemoParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.metas = []
        self.images = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "meta":
            self.metas.append(data)
        if tag == "img":
            self.images.append(data)

    def handle_data(self, data):
        self.text.append(data)


def test_demo_seydi_contract():
    html = PAGE.read_text(encoding="utf-8")
    parser = DemoParser()
    parser.feed(html)
    text = " ".join(parser.text).lower()

    robots = " ".join(
        meta.get("content", "").lower()
        for meta in parser.metas
        if meta.get("name", "").lower() == "robots"
    )
    assert "noindex" in robots and "nofollow" in robots and "noarchive" in robots
    assert "démo confidentielle" in text
    assert "saint-germain-lès-corbeil" in text
    assert "corbeil-essonnes" in text
    assert "265 000 €" in text
    assert "179 900 €" in text
    assert "document non contractuel" in text
    assert "géorisques" in text

    property_images = [img for img in parser.images if "property-photo" in img.get("class", "")]
    assert len(property_images) == 21
    assert all(img.get("alt", "").strip() for img in property_images)
    assert sum(img.get("loading") == "eager" for img in property_images) == 2
    assert sum(img.get("loading") == "lazy" for img in property_images) == 19
    assert all(img.get("src", "").endswith(".webp") for img in property_images)

    assets = ROOT / "demo-seydi" / "assets"
    assert len(list(assets.glob("saint-germain-*.webp"))) == 13
    assert len(list(assets.glob("corbeil-*.webp"))) == 8
    assert not list((ROOT / "demo-seydi").rglob("*.pdf"))
