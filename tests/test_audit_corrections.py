from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FR = (ROOT / "index.html").read_text(encoding="utf-8")
EN = (ROOT / "en" / "index.html").read_text(encoding="utf-8")
CASE_STUDY = (ROOT / "case-study" / "index.html").read_text(encoding="utf-8")
LEGAL = (ROOT / "mentions-legales" / "index.html").read_text(encoding="utf-8")
SITEMAP = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
HOME_CSS = (ROOT / "css" / "home.css").read_text(encoding="utf-8")
QUARTERLY = (ROOT / "revue-trimestrielle-powerpoint" / "index.html").read_text(encoding="utf-8")
EXTRACTOR = (ROOT / "extracteur-donnees-publiques" / "index.html").read_text(encoding="utf-8")


def test_language_choice_never_redirects_automatically():
    for html in (FR, EN, CASE_STUDY):
        assert "navigator.language" not in html
        assert "navigator.languages" not in html
        assert "location.replace" not in html


def test_french_and_english_homepage_prices_are_synchronized():
    # 3 cartes offre homepage : déploiement 50€, accompagnement 150€, supervision 15–29€/mois
    fr_prices = re.findall(r'class="offer-price[^>]*>(\d+)€<', FR)
    en_prices = re.findall(r'class="offer-price[^>]*>€(\d+)<', EN)
    assert fr_prices == ["50", "150"]
    assert en_prices == fr_prices
    # fourchette supervision synchronisée FR/EN
    assert re.search(r'15–29€', FR)
    assert re.search(r'€15–29', EN)


def test_alexandre_page_is_integrated_into_both_homepages_and_sitemap():
    for html in (FR, EN):
        assert 'href="/alexandre-lasly/"' in html
    assert "https://atlasnexus.tech/alexandre-lasly/" in SITEMAP


def test_legal_notice_names_actual_processors_and_purposes():
    assert "GoatCounter" in LEGAL
    assert "FormSubmit" in LEGAL
    assert "Hotjar" in LEGAL
    assert "mesure d'audience" in LEGAL
    assert "jamais cédées à des tiers" not in LEGAL
    assert "Aucun service d'analyse d'audience" not in LEGAL
    assert "+33 7 50 50 45 95" in LEGAL
    assert "adresse email, téléphone et contenu" not in LEGAL
    assert "entrepreneur individuel" not in LEGAL
    assert "éditeur du site" in LEGAL


def test_sitemap_prioritizes_offers_and_cases_not_raw_demos():
    assert "demo-refonte-artisan" not in SITEMAP
    assert "template-artisan" not in SITEMAP
    assert "client sites" not in SITEMAP.lower()
    assert "https://atlasnexus.tech/case-study/" in SITEMAP


def test_ai2work_copy_distinguishes_live_network_from_roadmap():
    for html in (FR, EN):
        assert "Celo Mainnet" in html
        assert "USDC" in html and "cUSD" in html and "CELO" in html
    assert "Multi-chain : Celo, Base, Polygon + Solana" not in FR
    assert "other networks are on the roadmap" in EN
    assert "ai2work.onrender.com" not in FR + EN


def test_obsolete_offers_and_projects_are_not_promoted_or_indexed():
    obsolete_home_copy = (
        "Revue trimestrielle PowerPoint",
        "Extraction bornée depuis une source web publique",
        "Birdeye Sprint 4",
        "Nexus Scout SAP",
        "Solana Market Pulse",
    )
    for label in obsolete_home_copy:
        assert label not in FR
        assert label not in EN
    assert "revue-trimestrielle-powerpoint" not in SITEMAP
    assert 'name="robots" content="noindex,follow"' in QUARTERLY
    assert 'name="robots" content="noindex,follow"' in EXTRACTOR


def test_homepage_hero_uses_the_loaded_rubik_900_display_font():
    hero_rule = re.search(r"\.hero-title\s*\{([^}]*)\}", HOME_CSS)
    assert hero_rule
    declarations = hero_rule.group(1)
    assert "font-family: 'Rubik', sans-serif" in declarations
    assert "font-weight: 900" in declarations
    assert '/css/home.css?v=4' in FR
    assert '/css/home.css?v=4' in EN


if __name__ == "__main__":
    tests = [(name, value) for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for name, test in tests:
        test()
        print(f"PASS {name}")
