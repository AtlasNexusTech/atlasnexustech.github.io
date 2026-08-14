import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FR = (ROOT / "demos-web" / "index.html").read_text(encoding="utf-8")
EN = (ROOT / "demos-web" / "en" / "index.html").read_text(encoding="utf-8")


def _visible(html: str) -> str:
    html = re.sub(r"<script\b[^>]*>.*?</script>", " ", html, flags=re.I | re.S)
    html = re.sub(r"<style\b[^>]*>.*?</style>", " ", html, flags=re.I | re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


def _section(html: str, section_id: str) -> str:
    match = re.search(
        rf'<section[^>]*id="{re.escape(section_id)}"[^>]*>(.*?)</section>',
        html,
        re.S,
    )
    assert match, f"missing section #{section_id}"
    return match.group(1)


def test_french_page_presents_demos_honestly():
    visible = _visible(FR)
    assert "Réalisations web &amp; démos : Atlas Nexus" in FR
    assert "Des réalisations web pour voir ce que je sais construire" in visible
    assert "Ce ne sont pas des études de cas client" in visible

    obsolete_claims = (
        "Catalogue de preuves",
        "preuve commerciale",
        "La preuve avant le devis",
        "Pas de portfolio externe. Des preuves intégrées.",
        "Sites créés pour mes partenaires",
        "Commander maintenant: 75€",
        "Livraison sous 48h",
        "Satisfait ou remboursé sous 14 jours",
        "mailto:",
        "https://buy.stripe.com/",
    )
    for claim in obsolete_claims:
        assert claim not in FR

    demos = _section(FR, "sector-demos")
    assert demos.count('data-demo-card="sector"') == 8
    assert demos.count("Démo indépendante") == 8
    assert "06 83 09 05 16" not in demos
    assert "Depuis 1947" not in demos
    assert "depuis 1959" not in demos


def test_english_page_is_symmetric_and_discloses_french_demos():
    visible = _visible(EN)
    assert "Web work &amp; demos : Atlas Nexus" in EN
    assert "Web work that shows what I can build" in visible
    assert "These are not client case studies" in visible
    assert not re.search(r"\b(we|our|us)\b", EN, re.I)

    demos = _section(EN, "sector-demos")
    assert demos.count('data-demo-card="sector"') == 8
    assert demos.count("Independent demo") == 8
    assert demos.count("Demo in French") == 8
    assert "15 ans d'exp." not in demos
    assert "Peintre depuis" not in demos


def test_tools_and_current_offer_replace_obsolete_sales_blocks():
    for html, contact, price, request in (
        (FR, "/#contact", "À partir de 40€", "Discuter de mon build"),
        (EN, "/en/#contact", "Starting from €40", "Discuss my build"),
    ):
        tools = _section(html, "interfaces-tools")
        assert "Markets Dashboard" in tools
        assert "UI Design System" in tools
        assert "Atlas Data Toolkit" in tools
        assert "https://github.com/AtlasNexusTech/datatoolkit" in tools
        assert f'href="{contact}"' in html
        assert price in html
        assert request in html
        assert "75€" not in html
        assert "€75" not in html
        assert "mailto:" not in html
        assert "buy.stripe.com" not in html


def test_external_links_are_safe():
    for html in (FR, EN):
        for tag in re.findall(r'<a\b[^>]*href="https?://[^">]+"[^>]*>', html, re.I):
            assert 'target="_blank"' in tag
            rel = re.search(r'rel="([^"]+)"', tag)
            assert rel
            assert {"noopener", "noreferrer"}.issubset(set(rel.group(1).split()))
