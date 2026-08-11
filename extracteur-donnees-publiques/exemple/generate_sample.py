#!/usr/bin/env python3
"""Génère puis extrait un mini-catalogue 100 % synthétique de 10 pages."""
from __future__ import annotations

import csv
import json
import re
import zipfile
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source-pages"
FIELDS = [
    "record_id",
    "title",
    "category",
    "city",
    "price_eur",
    "availability",
    "updated_at",
    "source_url",
]
ROWS = [
    ("SYN-001", "Lampe de bureau", "Bureau", "Lille", "42.00", "disponible", "2026-07-28"),
    ("SYN-002", "Support écran", "Bureau", "Rennes", "59.00", "disponible", "2026-07-29"),
    ("SYN-003", "Clavier compact", "Informatique", "Nantes", "74.50", "rupture", "2026-07-29"),
    ("SYN-004", "Sacoche ordinateur", "Mobilité", "Lyon", "38.90", "disponible", "2026-07-30"),
    ("SYN-005", "Hub USB-C", "Informatique", "Paris", "49.90", "disponible", "2026-07-30"),
    ("SYN-006", "Carnet relié", "Papeterie", "Bordeaux", "18.00", "disponible", "2026-07-30"),
    ("SYN-007", "Webcam HD", "Informatique", "Toulouse", "69.00", "précommande", "2026-07-31"),
    ("SYN-008", "Gourde inox", "Mobilité", "Grenoble", "24.90", "disponible", "2026-07-31"),
    ("SYN-009", "Repose-poignets", "Bureau", "Strasbourg", "21.50", "disponible", "2026-07-31"),
    ("SYN-010", "Casque antibruit", "Bureau", "Marseille", "84.00", "rupture", "2026-08-01"),
]


def build_sources() -> None:
    SOURCE.mkdir(parents=True, exist_ok=True)
    for record_id, title, category, city, price, availability, updated_at in ROWS:
        html = f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>{escape(title)}</title></head>
<body><main class="product" data-record-id="{record_id}">
<h1>{escape(title)}</h1><p class="category">{escape(category)}</p>
<p class="city">{escape(city)}</p><data class="price" value="{price}">{price} €</data>
<p class="availability">{escape(availability)}</p><time datetime="{updated_at}">{updated_at}</time>
</main></body></html>"""
        (SOURCE / f"{record_id.lower()}.html").write_text(html, encoding="utf-8")


def text(pattern: str, html: str, field: str) -> str:
    match = re.search(pattern, html, flags=re.I | re.S)
    if not match:
        raise ValueError(f"champ absent: {field}")
    return re.sub(r"<[^>]+>", "", match.group(1)).strip()


def extract() -> list[dict[str, str]]:
    records = []
    for path in sorted(SOURCE.glob("*.html")):
        html = path.read_text(encoding="utf-8")
        record = {
            "record_id": text(r'data-record-id="([^"]+)"', html, "record_id"),
            "title": text(r"<h1>(.*?)</h1>", html, "title"),
            "category": text(r'class="category">(.*?)</p>', html, "category"),
            "city": text(r'class="city">(.*?)</p>', html, "city"),
            "price_eur": text(r'class="price" value="([^"]+)"', html, "price_eur"),
            "availability": text(r'class="availability">(.*?)</p>', html, "availability"),
            "updated_at": text(r'<time datetime="([^"]+)"', html, "updated_at"),
            "source_url": f"https://exemple.invalid/catalogue/{path.stem}/",
        }
        records.append(record)
    return records


def write_outputs(records: list[dict[str, str]]) -> None:
    with (ROOT / "exemple-extraction.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)
    (ROOT / "exemple-extraction.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (ROOT / "journal-execution.txt").write_text(
        "STATUT=SUCCES\nPAGES_LUES=10\nLIGNES_PRODUITES=10\nERREURS=0\nDONNEES=SYNTHETIQUES\n",
        encoding="utf-8",
    )


def bundle() -> None:
    files = [
        "extracteur_demo.py",
        "README.md",
        "exemple-extraction.csv",
        "exemple-extraction.json",
        "journal-execution.txt",
    ]
    with zipfile.ZipFile(ROOT / "exemple-extracteur-donnees-publiques.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for name in files:
            archive.write(ROOT / name, arcname=name)
        for path in sorted(SOURCE.glob("*.html")):
            archive.write(path, arcname=f"source-pages/{path.name}")


if __name__ == "__main__":
    build_sources()
    records = extract()
    write_outputs(records)
    bundle()
    print(f"OK: {len(records)} pages, {len(FIELDS)} champs, 0 erreur")
