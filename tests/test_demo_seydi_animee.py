from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "demo-seydi-animee"
PAGE = DEMO / "index.html"


class MotionParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.scripts = []
        self.links = []
        self.metas = []
        self.attrs = []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        self.attrs.append(data)
        if tag == "img":
            self.images.append(data)
        elif tag == "script":
            self.scripts.append(data.get("src", ""))
        elif tag == "link":
            self.links.append(data.get("href", ""))
        elif tag == "meta":
            self.metas.append(data)


def test_animated_demo_contract():
    html = PAGE.read_text(encoding="utf-8")
    parser = MotionParser()
    parser.feed(html)

    robots = " ".join(
        item.get("content", "").lower()
        for item in parser.metas
        if item.get("name", "").lower() == "robots"
    )
    assert {"noindex", "nofollow", "noarchive"}.issubset(set(robots.replace(",", " ").split()))
    assert "motion.css?v=3" in parser.links
    assert "motion.js?v=1" in parser.scripts
    assert any("motion-page" in item.get("class", "") for item in parser.attrs)
    assert sum("property-photo" in img.get("class", "") for img in parser.images) == 21
    assert all(
        img.get("src", "").startswith("../demo-seydi/assets/")
        for img in parser.images
        if "property-photo" in img.get("class", "")
    )
    assert not list(DEMO.rglob("*.webp"))

    css = (DEMO / "motion.css").read_text(encoding="utf-8")
    js = (DEMO / "motion.js").read_text(encoding="utf-8")
    assert "prefers-reduced-motion: reduce" in css
    assert "IntersectionObserver" in js
    assert "requestAnimationFrame" in js
    assert "motion-progress" in html
