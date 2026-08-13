from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

OFFERS = {
    "index.html": (
        ("Votre premier agent en production sous 24&nbsp;h", "50€", "https://buy.stripe.com/3cI7sKenygvyej95Qj1Fe04", "Payer 50€"),
        ("Accompagnement + écosystème multi-agentique", "90€", "https://buy.stripe.com/4gM6oGgvG9365MD2E71Fe05", "Payer 90€"),
        ("Supervision &amp; évolution continue", "29€", "https://buy.stripe.com/6oU5kCa7i936grhdiL1Fe07", "S'abonner à 29€/mois"),
    ),
    "en/index.html": (
        ("Your first agent in production within 24&nbsp;h", "€50", "https://buy.stripe.com/3cI7sKenygvyej95Qj1Fe04", "Pay €50"),
        ("Coaching + multi-agent ecosystem", "€90", "https://buy.stripe.com/4gM6oGgvG9365MD2E71Fe05", "Pay €90"),
        ("Supervision &amp; continuous evolution", "€29", "https://buy.stripe.com/6oU5kCa7i936grhdiL1Fe07", "Subscribe for €29/month"),
    ),
}


def test_each_homepage_offer_card_has_its_matching_verified_stripe_checkout():
    for route, expected in OFFERS.items():
        html = (ROOT / route).read_text(encoding="utf-8")
        offers = html.split("<!-- Offers -->", 1)[1].split("<!-- Garantie -->", 1)[0]
        articles = re.findall(r"<article\b[^>]*>(.*?)</article>", offers, re.DOTALL)
        assert len(articles) == 3
        for article, (title, price, checkout, label) in zip(articles, expected):
            assert title in article
            assert price in article
            assert f'href="{checkout}"' in article
            assert label in article
            assert "rendez-vous" not in article
            assert "data-calendly" not in article
        assert "150€" not in offers and "€150" not in offers
        assert "15–29€" not in offers and "€15–29" not in offers
