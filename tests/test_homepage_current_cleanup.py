from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FR = (ROOT / "index.html").read_text(encoding="utf-8")
EN = (ROOT / "en" / "index.html").read_text(encoding="utf-8")


def test_homepages_keep_the_diagnostic_and_remove_the_free_trial_offer():
    assert "Réserver mon diagnostic" in FR
    assert "Book my free 30-min diagnostic" in EN
    for html in (FR, EN):
        assert 'href="/essai/"' not in html
    for text in (
        "Tester gratuitement",
        "accès d'essai gratuit",
        "Essai gratuit 7 jours",
        "Try it free",
        "free trial access",
        "Free 7-day trial",
    ):
        assert text not in FR
        assert text not in EN


def test_free_trial_routes_and_styles_are_removed_from_the_site():
    assert not (ROOT / "essai" / "index.html").exists()
    assert not (ROOT / "essai" / "espace" / "index.html").exists()
    assert "/essai/" not in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    css = (ROOT / "css" / "v2.css").read_text(encoding="utf-8")
    assert ".trial-" not in css
    assert ".ws-" not in css


def test_homepages_do_not_use_the_four_client_availability_claim():
    assert "4 clients par mois" not in FR
    assert "4 clients a month" not in EN


def test_homepages_do_not_promote_hermes_trading_agents():
    for html in (FR, EN):
        assert "HermesTradingAgents" not in html
        assert "AtlasNexusTech/HermesTradingAgents" not in html
