from __future__ import annotations

import re
import runpy
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://atlasnexus.tech"
EXTERNAL_INDEXABLE_URLS = {f"{DOMAIN}/alexandre-lasly/"}
NS = {
    "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
    "xhtml": "http://www.w3.org/1999/xhtml",
}


class SeoMetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.robots: list[str] = []
        self.refresh = False
        self.canonical = ""
        self.title_parts: list[str] = []
        self.in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_map = {str(key).lower(): (value or "") for key, value in attrs}
        tag = tag.lower()
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            if attrs_map.get("name", "").lower() in {"robots", "googlebot"}:
                self.robots.append(attrs_map.get("content", "").lower())
            if attrs_map.get("http-equiv", "").lower() == "refresh":
                self.refresh = True
        elif tag == "link" and "canonical" in attrs_map.get("rel", "").lower():
            self.canonical = attrs_map.get("href", "").strip()

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data.strip())


def sitemap_urls() -> list[str]:
    root = ET.parse(ROOT / "sitemap.xml").getroot()
    urls: list[str] = []
    for url_element in root.findall("sm:url", NS):
        loc = url_element.findtext("sm:loc", default="", namespaces=NS).strip()
        if loc:
            urls.append(loc)
        for alternate in url_element.findall("xhtml:link", NS):
            href = (alternate.attrib.get("href") or "").strip()
            if href:
                urls.append(href)
    return list(dict.fromkeys(urls))


def local_page(url: str) -> Path:
    parsed = urlparse(url)
    assert f"{parsed.scheme}://{parsed.netloc}" == DOMAIN, url
    route = parsed.path.strip("/")
    return ROOT / route / "index.html" if route else ROOT / "index.html"


def parse_page(path: Path) -> SeoMetaParser:
    parser = SeoMetaParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def test_sitemap_contains_only_existing_indexable_pages() -> None:
    errors: list[str] = []
    for url in sitemap_urls():
        if url in EXTERNAL_INDEXABLE_URLS:
            continue
        path = local_page(url)
        if not path.exists():
            errors.append(f"missing page: {url} -> {path.relative_to(ROOT)}")
            continue
        meta = parse_page(path)
        directives = ",".join(meta.robots)
        if "noindex" in directives:
            errors.append(f"noindex in sitemap: {url}")
        if meta.refresh:
            errors.append(f"meta-refresh redirect in sitemap: {url}")
        if meta.canonical and meta.canonical.rstrip("/") != url.rstrip("/"):
            errors.append(f"canonical mismatch in sitemap: {url} -> {meta.canonical}")
        if "chargement" in " ".join(meta.title_parts).lower():
            errors.append(f"loading shell in sitemap: {url}")
    assert not errors, "\n".join(errors)


def test_known_utility_private_and_redirect_routes_are_not_in_sitemap() -> None:
    content = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    excluded = {
        "/atlas-studio/",
        "/control-room/",
        "/demo-seydi/",
        "/demo-seydi-animee/",
        "/eponia-conseil/",
        "/merci/",
        "/pwa-template/",
    }
    leaked = sorted(route for route in excluded if f"{DOMAIN}{route}" in content)
    assert not leaked, f"non-indexable routes leaked into sitemap: {leaked}"


def test_hreflang_alternates_are_also_canonical_sitemap_entries() -> None:
    root = ET.parse(ROOT / "sitemap.xml").getroot()
    locs = {
        element.findtext("sm:loc", default="", namespaces=NS).strip()
        for element in root.findall("sm:url", NS)
    }
    alternates = {
        (link.attrib.get("href") or "").strip()
        for element in root.findall("sm:url", NS)
        for link in element.findall("xhtml:link", NS)
    }
    missing = sorted(alternates - locs)
    assert not missing, f"hreflang alternates missing their own <url><loc>: {missing}"


def test_committed_sitemap_matches_the_indexability_aware_generator() -> None:
    namespace = runpy.run_path(str(ROOT / "generate_sitemap.py"))
    generated = namespace["build_sitemap"]()
    committed = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert generated == committed


def test_robots_explicitly_allows_google_indexing_agents() -> None:
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    for agent in ("Googlebot", "Googlebot-Image", "Google-InspectionTool"):
        pattern = rf"(?ims)^User-agent:\s*{re.escape(agent)}\s*$.*?^Allow:\s*/\s*$"
        assert re.search(pattern, robots), f"missing explicit Allow: / for {agent}"
    assert "Sitemap: https://atlasnexus.tech/sitemap.xml" in robots
