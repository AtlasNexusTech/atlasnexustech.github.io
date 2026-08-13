import html
import json
import re
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    ("relative_path", "new_timing", "obsolete_timing"),
    [
        ("ia-agentique/index.html", "en 20 minutes", "en 24 heures"),
        ("ia-agentique/en/index.html", "in 20 minutes", "in 24 hours"),
    ],
)
def test_ia_agentique_hero_promises_twenty_minute_delivery(
    relative_path, new_timing, obsolete_timing
):
    html = (ROOT / relative_path).read_text(encoding="utf-8")
    hero = html.split("</h1>", 1)[0]

    assert new_timing in hero
    assert obsolete_timing not in hero


@pytest.mark.parametrize(
    ("relative_path", "no_commitment_copy"),
    [
        ("ia-agentique/index.html", "Sans engagement"),
        ("ia-agentique/en/index.html", "No commitment"),
    ],
)
def test_ia_agentique_has_four_deployment_and_managed_service_offers(
    relative_path, no_commitment_copy
):
    html = (ROOT / relative_path).read_text(encoding="utf-8")

    scripts = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL
    )
    parsed_scripts = [json.loads(script) for script in scripts]
    service = next(data for data in parsed_scripts if data.get("@type") == "Service")

    assert service["offers"] == {
        "@type": "AggregateOffer",
        "priceCurrency": "EUR",
        "lowPrice": "15",
        "highPrice": "90",
        "offerCount": "4",
        "availability": "https://schema.org/InStock",
        "url": "https://atlasnexus.tech/ia-agentique/",
    }

    pricing_section = html.split('<section id="pricing"', 1)[1].split("</section>", 1)[0]
    assert pricing_section.count("pricing-card") == 4
    pricing_lower = pricing_section.lower()
    assert ">50€" in pricing_section or ">€50" in pricing_section
    assert ">90€" in pricing_section or ">€90" in pricing_section
    assert "15€" in pricing_section or "€15" in pricing_section
    assert "29€" in pricing_section or "€29" in pricing_section
    assert no_commitment_copy.lower() in pricing_lower
    assert "telegram" in pricing_lower
    assert "infrastructure" in pricing_lower
    assert "clé en main" in pricing_lower or "turnkey" in pricing_lower

    assert ">5€</p>" not in pricing_section
    assert "coaching" not in html.lower()

    # liens de paiement Stripe réels présents
    assert html.count("https://buy.stripe.com/") >= 4
    assert "https://atlasnexus.tech/merci/" in html or "buy.stripe.com" in html

    for obsolete in (
        "150€",
        "350€",
        "50€/h",
        "20€",
        "75€",
        "20€/h",
        "Agents Connectés",
        "Agent Connecté",
        "Connected Agents",
        "Connected Agent",
    ):
        assert obsolete not in html

    assert "✨" not in html


def _visible_text(fragment):
    return html.unescape(" ".join(re.sub(r"<[^>]+>", " ", fragment).split()))


def _anchor_attributes(container, visible_label):
    matches = []
    for anchor in re.finditer(r"<a\s+([^>]*)>(.*?)</a>", container, re.DOTALL):
        if _visible_text(anchor.group(2)) == visible_label:
            matches.append(anchor.group(1))
    assert len(matches) == 1, f"Expected one anchor labelled {visible_label!r}"
    return matches[0]


def _article_with_heading(container, heading):
    matches = []
    for article in re.findall(r"<article\b[^>]*>(.*?)</article>", container, re.DOTALL):
        title = re.search(r"<h3\b[^>]*>(.*?)</h3>", article, re.DOTALL)
        if title is not None and _visible_text(title.group(1)) == heading:
            matches.append(article)
    assert len(matches) == 1, f"Expected one article headed {heading!r}"
    return matches[0]


@pytest.mark.parametrize(
    (
        "relative_path",
        "hero_label",
        "card_1_title",
        "card_1_price",
        "card_2_title",
        "card_2_price",
        "card_3_title",
        "card_3_price",
    ),
    [
        (
            "index.html",
            "Réserver mon diagnostic",
            "Votre premier agent en production sous 24\u00a0h",
            "50€",
            "Accompagnement + écosystème multi-agentique",
            "150€",
            "Supervision & évolution continue",
            "15–29€",
        ),
        (
            "en/index.html",
            "Book my free 30-min diagnostic",
            "Your first agent in production within 24\u00a0h",
            "€50",
            "Coaching + multi-agent ecosystem",
            "€150",
            "Supervision & continuous evolution",
            "€15–29",
        ),
    ],
)
def test_homepage_promotes_the_current_agent_offer(
    relative_path,
    hero_label,
    card_1_title,
    card_1_price,
    card_2_title,
    card_2_price,
    card_3_title,
    card_3_price,
):
    html = (ROOT / relative_path).read_text(encoding="utf-8")
    hero_match = re.search(r'<!-- Hero -->(.*?)<!-- AvantApres -->', html, re.DOTALL)
    offers_match = re.search(r'<!-- Offers -->(.*?)<!-- Garantie -->', html, re.DOTALL)
    assert hero_match is not None
    assert offers_match is not None
    hero = hero_match.group(1)
    offers = offers_match.group(1)

    # Hero : CTA diagnostic (route de contact principale de la refonte)
    primary = _anchor_attributes(hero, hero_label)
    assert 'href="#contact"' in primary
    assert "bg-primary" in primary

    # 3 cartes d'offre avec les prix réels
    card_1 = _article_with_heading(offers, card_1_title)
    assert card_1_price in _visible_text(card_1)
    card_2 = _article_with_heading(offers, card_2_title)
    assert card_2_price in _visible_text(card_2)
    card_3 = _article_with_heading(offers, card_3_title)
    assert card_3_price in _visible_text(card_3)

    assert re.search(r"\bDiscord\b", offers, re.IGNORECASE) is None
    assert re.search(r"(?:10\s*€|€\s*10)", offers) is None


@pytest.mark.parametrize(
    ("relative_path", "sticky_label"),
    [
        ("index.html", "Diagnostic 30 min gratuit →"),
        ("en/index.html", "Free 30-min diagnostic →"),
    ],
)
def test_homepage_mobile_sticky_cta_targets_the_fixed_price_offer(
    relative_path, sticky_label
):
    html = (ROOT / relative_path).read_text(encoding="utf-8")
    sticky = re.search(
        r'<a href="([^"]+)" class="fixed bottom-4[^>]*>(.*?)</a>', html, re.DOTALL
    )
    assert sticky is not None
    assert sticky.group(1) == "#contact"
    assert sticky.group(2).strip() == sticky_label


@pytest.mark.parametrize(
    ("relative_path", "offer_values", "status_copy"),
    [
        (
            "ia-agentique/index.html",
            {
                "infra": "Déploiement sur votre infrastructure 50€",
                "cle-en-main": "Déploiement clé en main 90€",
                "maintenance": "Maintenance essentielle 15€/mois",
                "infogerance": "Infogérance complète 29€/mois",
            },
            "Offre présélectionnée :",
        ),
        (
            "ia-agentique/en/index.html",
            {
                "infra": "Deployment on your infrastructure €50",
                "cle-en-main": "Turnkey deployment €90",
                "maintenance": "Essential maintenance €15/month",
                "infogerance": "Full managed service €29/month",
            },
            "Preselected offer:",
        ),
    ],
)
def test_offer_links_prefill_the_matching_form_option(
    relative_path, offer_values, status_copy
):
    html = (ROOT / relative_path).read_text(encoding="utf-8")

    offer_links = [
        attributes
        for attributes in re.findall(r"<a\s+([^>]*)>", html)
        if 'data-offer="' in attributes
    ]
    assert len(offer_links) == 9
    for offer in offer_values:
        assert sum(f'data-offer="{offer}"' in attributes for attributes in offer_links) >= 2
    for attributes in offer_links:
        offer_match = re.search(r'data-offer="([a-z-]+)"', attributes)
        assert offer_match is not None
        offer = offer_match.group(1)
        assert offer in offer_values
        assert f'href="?offer={offer}#order-form"' in attributes

    assert 'id="offer-select"' in html
    assert 'for="offer-select"' in html
    for offer, value in offer_values.items():
        assert f'<option value="{value}">' in html
    assert 'id="offer-prefill-status"' in html
    assert 'aria-live="polite"' in html

    assert "new URLSearchParams(window.location.search)" in html
    assert "params.get('offer')" in html
    for offer, value in offer_values.items():
        assert value in html
        assert re.search(rf"(?:'?{re.escape(offer)}'?\s*:\s*'{re.escape(value)}')", html) is not None
    assert "Object.prototype.hasOwnProperty.call(offers, selectedOffer)" in html
    assert "offerSelect.value = offers[selectedOffer]" in html
    assert "status.textContent =" in html
    assert status_copy in html

    assert "Formulaire sécurisé" not in html
    assert "Secure form" not in html


@pytest.mark.parametrize(
    ("relative_path", "fields"),
    [
        (
            "ia-agentique/index.html",
            (
                ("customer-name", "nom"),
                ("customer-email", "email"),
                ("customer-project", "entreprise"),
                ("offer-select", "offre"),
                ("customer-need", "besoin"),
                ("preferred-platform", "plateforme"),
            ),
        ),
        (
            "ia-agentique/en/index.html",
            (
                ("customer-name", "name"),
                ("customer-email", "email"),
                ("customer-project", "company"),
                ("offer-select", "offre"),
                ("customer-need", "need"),
                ("preferred-platform", "platform"),
            ),
        ),
    ],
)
def test_contact_form_labels_are_associated_with_their_controls(relative_path, fields):
    html = (ROOT / relative_path).read_text(encoding="utf-8")

    for control_id, field_name in fields:
        assert f'<label for="{control_id}"' in html
        control = re.search(
            rf'<(?:input|select|textarea)[^>]*id="{re.escape(control_id)}"[^>]*name="{re.escape(field_name)}"',
            html,
        )
        assert control is not None

    assert 'id="customer-name" type="text" name=' in html
    assert 'autocomplete="name"' in html
    assert 'id="customer-email" type="email" name="email" autocomplete="email"' in html
    assert 'id="customer-project" type="text" name=' in html
    assert 'autocomplete="organization"' in html

    assert "Formulaire sécurisé" not in html
    assert "Secure form" not in html
