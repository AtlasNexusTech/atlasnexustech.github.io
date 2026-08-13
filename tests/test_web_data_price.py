import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "index.html"
OFFER = ROOT / "developpement-web-donnees" / "index.html"


def test_web_data_offer_starts_at_forty_euros_everywhere():
    home = HOME.read_text(encoding="utf-8")
    offer = OFFER.read_text(encoding="utf-8")

    # La refonte a retiré la carte « Développement web, données » de la homepage
    # — la page offre dédiée reste la source du prix 40€ (dans le sitemap).
    assert "Développement web" in home
    assert '"price": "40"' in offer
    assert "40€" in offer
    assert "Commander maintenant : à partir de 40€" in offer
    assert "150€" not in offer
    assert '"price": "90"' not in offer

    json_ld_match = re.search(
        r'<script type="application/ld\+json">(.*?)</script>',
        offer,
        flags=re.DOTALL,
    )
    assert json_ld_match
    payload = json.loads(json_ld_match.group(1))
    assert payload["offers"]["price"] == "40"
    assert payload["offers"]["priceCurrency"] == "EUR"
