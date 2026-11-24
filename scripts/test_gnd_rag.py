
import json
import time
from pathlib import Path

import requests

MODEL = "gemma3:4b"

# Dokument und GND-Suchergebnisse laden
document = Path(
    "data/processed/eu_partnerships.txt"
).read_text(encoding="utf-8")

search_results = json.loads(
    Path("data/processed/gnd_candidates.json")
    .read_text(encoding="utf-8")
)

# Eindeutige GND-Kandidaten zusammenstellen
candidates = {}

for search in search_results:
    if search.get("error"):
        raise RuntimeError(
            f"GND-Suche fehlgeschlagen: {search['keyword']}"
        )

    for item in search["candidates"]:
        if item.get("id") and item.get("preferredName"):
            candidates[item["id"]] = {
                "preferredName": item["preferredName"],
                "id": item["id"],
            }

candidate_list = list(candidates.values())

print(f"GND-Kandidaten: {len(candidate_list)}")

prompt = f"""
You are a subject indexing assistant for an academic library.

Your task is to select exactly five appropriate GND
subject headings for the document below.

You may ONLY select headings from the provided list
of verified GND candidates.

Do not invent GND identifiers or preferred names.

Select headings based on their relevance to the
document's main subjects, not merely word overlap.

If fewer than five candidates are genuinely relevant,
return fewer than five rather than adding unsuitable ones.

Return ONLY valid JSON in the following structure:

{{
  "subjects": [
    {{
      "preferredName": "Exact GND preferred name",
      "id": "Exact GND URI",
      "reason": "Brief explanation in English"
    }}
  ]
}}

GND CANDIDATES:
{json.dumps(candidate_list, ensure_ascii=False, indent=2)}

DOCUMENT:
{document}
"""

print(f"Starte {MODEL} mit GND-Retrieval ...")

start = time.time()

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0,
            "num_ctx": 16384,
            "num_predict": 1000,
        },
    },
    timeout=600,
)

response.raise_for_status()
result = response.json()

duration = time.time() - start

# Modellantwort als JSON parsen
output = json.loads(result["response"])

# GND-IDs und Benennungen überprüfen
verified = []
errors = []

for subject in output.get("subjects", []):
    gnd_id = subject.get("id")
    name = subject.get("preferredName")

    if (
        gnd_id in candidates
        and candidates[gnd_id]["preferredName"] == name
    ):
        verified.append(subject)
    else:
        errors.append(subject)

# Ergebnisse speichern
report = {
    "model": MODEL,
    "runtime_seconds": round(duration, 1),
    "prompt_tokens": result.get("prompt_eval_count"),
    "output_tokens": result.get("eval_count"),
    "retrieved_candidates": len(candidate_list),
    "verified_subjects": verified,
    "invalid_subjects": errors,
}

path = Path("data/processed/gnd_rag_result.json")
path.write_text(
    json.dumps(report, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

print("\n--- VERIFIZIERTE GND-SCHLAGWÖRTER ---")

for subject in verified:
    print(f"\n{subject['preferredName']}")
    print(subject["id"])
    print(subject.get("reason", ""))

print("\n--- STATISTIK ---")
print("Laufzeit:", round(duration, 1), "Sekunden")
print("Prompt-Tokens:", result.get("prompt_eval_count"))
print("Output-Tokens:", result.get("eval_count"))
print("Verifizierte Schlagwörter:", len(verified))
print("Ungültige Ausgaben:", len(errors))
print("Ergebnis gespeichert:", path)

