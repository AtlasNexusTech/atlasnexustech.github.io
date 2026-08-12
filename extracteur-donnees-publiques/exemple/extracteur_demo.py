#!/usr/bin/env python3
"""Extrait 8 champs depuis les 10 pages HTML synthétiques incluses."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source-pages"
FIELDS = ["record_id", "title", "category", "city", "price_eur", "availability", "updated_at", "source_url"]


def capture(pattern: str, html: str, field: str) -> str:
    match = re.search(pattern, html, flags=re.I | re.S)
    if not match:
        raise ValueError(f"champ absent: {field}")
    return re.sub(r"<[^>]+>", "", match.group(1)).strip()


def extract(path: Path) -> dict[str, str]:
    html = path.read_text(encoding="utf-8")
    return {
        "record_id": capture(r'data-record-id="([^"]+)"', html, "record_id"),
        "title": capture(r"<h1>(.*?)</h1>", html, "title"),
        "category": capture(r'class="category">(.*?)</p>', html, "category"),
        "city": capture(r'class="city">(.*?)</p>', html, "city"),
        "price_eur": capture(r'class="price" value="([^"]+)"', html, "price_eur"),
        "availability": capture(r'class="availability">(.*?)</p>', html, "availability"),
        "updated_at": capture(r'<time datetime="([^"]+)"', html, "updated_at"),
        "source_url": f"https://exemple.invalid/catalogue/{path.stem}/",
    }


def main() -> None:
    records = [extract(path) for path in sorted(SOURCE.glob("*.html"))]
    if len(records) != 10:
        raise SystemExit(f"10 pages attendues, {len(records)} trouvées")
    with (ROOT / "exemple-extraction.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)
    (ROOT / "exemple-extraction.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "journal-execution.txt").write_text(
        "STATUT=SUCCES\nPAGES_LUES=10\nLIGNES_PRODUITES=10\nERREURS=0\nDONNEES=SYNTHETIQUES\n",
        encoding="utf-8",
    )
    print("OK: 10 pages, 8 champs, 0 erreur")


if __name__ == "__main__":
    main()
