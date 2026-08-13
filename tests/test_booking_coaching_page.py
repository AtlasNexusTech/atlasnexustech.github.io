from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "rendez-vous" / "index.html"
BOOKING_JS = (ROOT / "js" / "booking.js").read_text(encoding="utf-8")
PDF = ROOT / "assets" / "documents" / "nexus-preparation-coaching.pdf"
HOME = (ROOT / "index.html").read_text(encoding="utf-8")


def test_booking_page_explains_coaching_value_and_process():
    html = PAGE.read_text(encoding="utf-8")
    for required in (
        'lang="fr"',
        "Pourquoi me contacter",
        "Ce que ce coaching va vous apporter",
        "Comment se déroule le rendez-vous",
        "Votre document préparatoire Nexus",
        "30 minutes",
        "Sans engagement",
    ):
        assert required in html


def test_booking_page_embeds_the_existing_calendly_event():
    html = PAGE.read_text(encoding="utf-8")
    assert "https://calendly.com/laslyalexandre/30min" in html
    assert "calendly-inline-widget" in html
    assert "https://assets.calendly.com/assets/external/widget.js" in html
    assert "Calendly.isCalendlyEvent" in BOOKING_JS
    assert "calendly.event_scheduled" in BOOKING_JS


def test_preparation_document_is_offered_after_scheduling_with_manual_fallback():
    html = PAGE.read_text(encoding="utf-8")
    assert 'id="booking-confirmed"' in html
    assert 'hidden' in html
    assert 'href="/assets/documents/nexus-preparation-coaching.pdf?v=1"' in html
    assert 'download="Nexus-preparation-coaching.pdf"' in html
    assert "sessionStorage" in BOOKING_JS
    assert PDF.exists()
    reader = PdfReader(str(PDF))
    assert len(reader.pages) >= 2
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    for required in ("Préparation Nexus", "Votre objectif", "Situation actuelle", "Priorités", "Indicateurs de réussite"):
        assert required in text


def test_homepage_primary_booking_paths_use_the_dedicated_page():
    assert HOME.count('href="/rendez-vous/"') >= 3
