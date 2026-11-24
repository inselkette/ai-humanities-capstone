
import requests
import json
from pathlib import Path

# Schlagwörter aus dem Gemma-3-4B-Experiment
keywords = [
    "Entwicklungszusammenarbeit",
    "Globale Partnerschaften",
    "Nachhaltigkeit",
    "Geopolitik",
    "Investitionsstrategie",
]

# Speicherort für die Ergebnisse
output = Path("data/processed/gnd_candidates.json")
output.parent.mkdir(parents=True, exist_ok=True)

results = []

for keyword in keywords:
    print(f"\n{'=' * 60}")
    print(f"Suchbegriff: {keyword}")
    print("=" * 60)

    try:
        response = requests.get(
            "https://lobid.org/gnd/search",
            params={
                "q": keyword,
                "filter": "type:SubjectHeading",
                "size": 10,
                "format": "json",
            },
            headers={
                "User-Agent": "ai-humanities-capstone/0.1"
            },
            timeout=30,
        )

        response.raise_for_status()
        data = response.json()

        candidates = []

        for item in data.get("member", []):
            candidate = {
                "preferredName": item.get("preferredName"),
                "id": item.get("id"),
                "type": item.get("type"),
            }

            candidates.append(candidate)

        results.append({
            "keyword": keyword,
            "candidates": candidates,
        })

        if not candidates:
            print("Keine passenden GND-Sachbegriffe gefunden.")
        else:
            for i, candidate in enumerate(candidates, start=1):
                print(
                    f"{i}. {candidate['preferredName']}\n"
                    f"   GND: {candidate['id']}\n"
                    f"   Typ: {candidate['type']}"
                )

    except requests.RequestException as error:
        print(f"Fehler bei der GND-Abfrage: {error}")

        results.append({
            "keyword": keyword,
            "candidates": [],
            "error": str(error),
        })

# Ergebnisse als JSON speichern
output.write_text(
    json.dumps(
        results,
        ensure_ascii=False,
        indent=2,
    ),
    encoding="utf-8",
)

print(f"\nErgebnisse gespeichert unter: {output}")

