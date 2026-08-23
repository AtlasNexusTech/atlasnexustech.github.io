"""Generate the canonical XML sitemap for atlasnexus.tech.

Only indexable HTML pages are included. Private demos, utility routes,
meta-refresh aliases and pages carrying a noindex directive are deliberately
excluded so Google receives one coherent indexing signal.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from html import escape
from html.parser import HTMLParser
from pathlib import Path

BASE = Path(__file__).resolve().parent
DOMAIN = "https://atlasnexus.tech"
OUTPUT = BASE / "sitemap.xml"

# This route is served outside this repository but is linked from both
# homepages and has a live, indexable canonical page.
SPECIAL_INDEXABLE_ROUTES = {"/alexandre-lasly/"}

HIGH_PRIORITY_ROUTES = {
    "/ia-agentique/",
    "/en/ia-agentique/",
    "/developpement-web-donnees/",
    "/en/developpement-web-donnees/",
    "/training/",
    "/en/training/",
    "/alexandre-lasly/",
}


class SeoMetadataParser(HTMLParser):
    """Read indexability metadata without adding an HTML dependency."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.robots: list[str] = []
        self.has_meta_refresh = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "meta":
            return
        attrs_map = {str(key).lower(): (value or "") for key, value in attrs}
        if attrs_map.get("name", "").lower() in {"robots", "googlebot"}:
            self.robots.append(attrs_map.get("content", "").lower())
        if attrs_map.get("http-equiv", "").lower() == "refresh":
            self.has_meta_refresh = True

    @property
    def indexable(self) -> bool:
        return "noindex" not in ",".join(self.robots) and not self.has_meta_refresh


def route_for(page: Path) -> str:
    parent = page.relative_to(BASE).parent.as_posix()
    return "/" if parent == "." else f"/{parent.strip('/')}/"


def metadata_for(page: Path) -> SeoMetadataParser:
    parser = SeoMetadataParser()
    parser.feed(page.read_text(encoding="utf-8"))
    return parser


def discover_routes() -> set[str]:
    routes: set[str] = set(SPECIAL_INDEXABLE_ROUTES)
    for page in BASE.rglob("index.html"):
        relative = page.relative_to(BASE)
        if any(part.startswith(".") or part == "node_modules" for part in relative.parts):
            continue
        if metadata_for(page).indexable:
            routes.add(route_for(page))
    return routes


def language_pair(route: str, routes: set[str]) -> tuple[str, str] | None:
    """Return the French and English routes when both versions exist."""
    if route == "/":
        return ("/", "/en/") if "/en/" in routes else None
    if route == "/en/":
        return ("/", "/en/") if "/" in routes else None

    path = route.strip("/")
    if path.startswith("en/"):
        french = f"/{path[3:]}/"
        return (french, route) if french in routes else None
    if path.endswith("/en"):
        french = f"/{path[:-3]}/"
        return (french, route) if french in routes else None

    english_prefix = f"/en/{path}/"
    english_suffix = f"/{path}/en/"
    if english_prefix in routes:
        return (route, english_prefix)
    if english_suffix in routes:
        return (route, english_suffix)
    return None


def priority(route: str) -> str:
    if route in {"/", "/en/"}:
        return "1.0"
    if route in HIGH_PRIORITY_ROUTES:
        return "0.9"
    if route.startswith("/en/") or route.endswith("/en/"):
        return "0.8"
    return "0.7"


def url(value: str) -> str:
    return escape(f"{DOMAIN}{value}", quote=True)


def build_sitemap(routes: set[str] | None = None) -> str:
    routes = discover_routes() if routes is None else set(routes)
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]

    sorted_routes = sorted(routes, key=lambda route: (route != "/", route))
    for route in sorted_routes:
        pair = language_pair(route, routes)
        if pair:
            french, english = pair
            line = f"  <url><loc>{url(route)}</loc>"
            line += f'<xhtml:link rel="alternate" hreflang="fr" href="{url(french)}"/>'
            line += f'<xhtml:link rel="alternate" hreflang="en" href="{url(english)}"/>'
            line += f'<xhtml:link rel="alternate" hreflang="x-default" href="{url(french)}"/>'
            frequency = "weekly" if route in {"/", "/en/"} else "monthly"
            line += f"<changefreq>{frequency}</changefreq><priority>{priority(route)}</priority></url>"
        else:
            frequency = "weekly" if route == "/" else "monthly"
            line = f"  <url><loc>{url(route)}</loc>"
            line += f"<changefreq>{frequency}</changefreq><priority>{priority(route)}</priority></url>"
        lines.append(line)

    lines.append("</urlset>")
    content = "\n".join(lines) + "\n"
    ET.fromstring(content)
    return content


def main() -> None:
    content = build_sitemap()
    OUTPUT.write_text(content, encoding="utf-8")
    count = content.count("<url>")
    print(f"Sitemap generated: {count} canonical URL entries")
    print("XML valid")


if __name__ == "__main__":
    main()
