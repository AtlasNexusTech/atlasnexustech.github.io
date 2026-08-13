from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENGLISH_HOME = ROOT / "en" / "index.html"
FRENCH_HOME = ROOT / "index.html"
HOME_STYLES = ROOT / "css" / "home.css"


def test_homepages_share_the_same_visual_system():
    english_html = ENGLISH_HOME.read_text(encoding="utf-8")
    french_html = FRENCH_HOME.read_text(encoding="utf-8")
    css = HOME_STYLES.read_text(encoding="utf-8")

    assert 'href="/css/home.css?v=4"' in english_html
    assert 'href="/css/home.css?v=4"' in french_html
    assert ".hero-title { font-family: 'Rubik', sans-serif; font-size: clamp(3.2rem, 9vw, 7rem);" in css
    assert ".glow-word { position: relative; display: inline-block;" in css
    assert ".section-title { font-size: clamp(1.8rem, 4.5vw, 3rem);" in css
    # La navigation legacy (glass-nav) a été supprimée — seule la nav Atlas reste.
    assert 'class="glass-nav flex h-[50px] items-center' not in english_html
    assert 'class="glass-nav flex h-20 items-center' not in english_html


def test_english_home_has_no_known_french_copy_leaks():
    html = ENGLISH_HOME.read_text(encoding="utf-8")

    for obsolete_copy in (
        "données structurées",
        "indépendants, PME",
        "composants animés",
        "pages de vente",
        "Réponse sous 24h",
        "Devis gratuit",
        "Mentions légales",
    ):
        assert obsolete_copy not in html

    assert 'href="/demos-web/en/"' in html
