from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FR = (ROOT / "index.html").read_text(encoding="utf-8")
EN = (ROOT / "en" / "index.html").read_text(encoding="utf-8")
CSS = (ROOT / "css" / "home-solutions.css").read_text(encoding="utf-8")
DOCS_URL = "https://docs.openclaw.ai/install"


def _solutions_section(html: str) -> str:
    assert '<section id="solutions-agentiques"' in html
    return html.split('<section id="solutions-agentiques"', 1)[1].split(
        "</section>", 1
    )[0]


@pytest.mark.parametrize(
    ("html", "cta"),
    [
        (FR, "Voir le tutoriel d’installation"),
        (EN, "View the installation guide"),
    ],
)
def test_homepages_show_openclaw_beside_hermes_and_prime_agent(html: str, cta: str):
    section = _solutions_section(html)

    assert section.count('class="agent-solution-card ') == 3
    assert 'href="/hermes/"' in section
    assert 'href="/prime-agent/"' in section
    assert f'href="{DOCS_URL}"' in section
    assert 'target="_blank"' in section
    assert 'rel="noopener noreferrer"' in section
    assert 'src="/assets/openclaw-2-mascot.png"' in section
    assert "OpenClaw 2.0" in section
    assert cta in section


def test_openclaw_asset_and_three_column_layout_exist():
    assert (ROOT / "assets" / "openclaw-2-mascot.png").is_file()
    assert "grid-template-columns:repeat(3,minmax(0,1fr))" in CSS
    assert ".agent-solution-openclaw-visual" in CSS
