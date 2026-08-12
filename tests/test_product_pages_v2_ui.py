from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKETS = (ROOT / "markets-dashboard" / "index.html").read_text(encoding="utf-8")
DESK_FR = (ROOT / "atlas-desk" / "index.html").read_text(encoding="utf-8")
DESK_EN = (ROOT / "atlas-desk" / "en" / "index.html").read_text(encoding="utf-8")
PRODUCT_CSS = ROOT / "css" / "product-v2.css"


def test_product_pages_load_the_shared_atlas_v2_ui_layer():
    for html in (MARKETS, DESK_FR, DESK_EN):
        assert 'href="/css/product-v2.css?v=1"' in html
        assert 'atlas-product-v2' in html
        assert 'atlas-product-hero' in html
        assert 'atlas-product-primary' in html
        assert 'atlas-product-secondary' in html


def test_atlas_desk_language_switch_stays_in_product_context():
    assert '<a href="/atlas-desk/" data-atlas-lang="fr" aria-current="page">FR</a>' in DESK_FR
    assert '<a href="/atlas-desk/en/" data-atlas-lang="en">EN</a>' in DESK_FR
    assert '<a href="/atlas-desk/" data-atlas-lang="fr">FR</a>' in DESK_EN
    assert '<a href="/atlas-desk/en/" data-atlas-lang="en" aria-current="page">EN</a>' in DESK_EN


def test_english_product_mobile_ctas_are_localized_and_target_english_contact():
    for html in (MARKETS, DESK_EN):
        assert 'href="/en/#contact"' in html
        assert 'aria-label="Request an Atlas Nexus quote"' in html
        assert '>Request a quote →</a>' in html
        assert "Demander un devis" not in html


def test_markets_respects_reduced_motion_for_canvas_and_count_up():
    assert "const reduceMotion=window.matchMedia('(prefers-reduced-motion: reduce)').matches" in MARKETS
    assert "if(reduceMotion){c.style.display='none';return}" in MARKETS
    assert "if(window.matchMedia('(prefers-reduced-motion: reduce)').matches){" in MARKETS
    assert "el.textContent=Number(el.dataset.target||0).toLocaleString('en-US')" in MARKETS
    assert "console.log('Canvas initialized'" not in MARKETS


def test_shared_product_ui_covers_brand_surfaces_responsiveness_and_accessibility():
    assert PRODUCT_CSS.exists()
    css = PRODUCT_CSS.read_text(encoding="utf-8")
    for selector in (
        ".atlas-product-v2",
        ".atlas-product-hero",
        ".atlas-product-primary",
        ".atlas-product-secondary",
        ".atlas-product-panel",
        ".atlas-product-v2 .highlight-card",
        ".atlas-product-v2 .market-card",
        "@media (max-width: 720px)",
        "@media (max-width: 639px)",
        "padding-bottom: 5.75rem",
        "@media (prefers-reduced-motion: reduce)",
        ":focus-visible",
        "html.dark",
    ):
        assert selector in css


def test_product_pages_use_the_compact_shared_header_without_visible_legacy_navigation():
    for html in (MARKETS, DESK_FR, DESK_EN):
        assert html.count("data-atlas-site-header") == 1
        assert 'data-atlas-legacy-nav aria-hidden="true" inert' in html
        assert 'atlas-unified-header' in html
