
import json
import time
from pathlib import Path

import requests

MODEL = "gemma3:4b"
DATA_DIR = Path("data/processed")

# Dokument laden
document = (
    DATA_DIR / "eu_partnerships.txt"
).read_text(encoding="utf-8")

# GND-Kandidaten laden
search_results = json.loads(
    (DATA_DIR / "gnd_candidates.json").read_text(
        encoding="utf-8"
    )
)

# Kandidaten deduplizieren
unique_candidates = {}

for search in search_results:
    if search.get("error"):
        raise RuntimeError(
            f"GND search failed for: {search['keyword']}"
        )

    for item in search["candidates"]:
        if item.get("id") and item.get("preferredName"):
            unique_candidates[item["id"]] = item

# Interne Kandidatennummern vergeben
candidates = {}

for i, item in enumerate(unique_candidates.values(), 1):
    code = f"C{i:02d}"
    candidates[code] = {
        "preferredName": item["preferredName"],
        "id": item["id"],
    }

# Kandidatenliste für Gemma
candidate_text = "\n".join(
    f"{code} | {item['preferredName']}"
    for code, item in candidates.items()
)

print(f"GND-Kandidaten: {len(candidates)}")

prompt = f"""
You are an expert in subject indexing for academic libraries.

Select up to five GND subject headings that best describe
the main subjects of the document.

You must select ONLY from the candidate list below.

IMPORTANT RULES:

- Return only candidate codes (e.g. C01, C04).
- Do not generate GND identifiers.
- Do not generate subject heading names.
- Do not select headings based on superficial associations.
- Every selected heading must describe a central subject.
- Do not select religious, artistic, or historical subjects
  unless they are explicitly central to the document.
- If fewer than five headings are suitable, select fewer.
- Do not invent candidate codes.

Return ONLY valid JSON:

{{
  "selected": ["C01", "C04"]
}}

AVAILABLE GND CANDIDATES:

{candidate_text}

DOCUMENT:

{document}
"""

print(f"Starte {MODEL} – GND Retrieval v2 ...")

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
            "num_predict": 300,
        },
    },
    timeout=600,
)

response.raise_for_status()
result = response.json()

duration = time.time() - start
model_output = json.loads(result["response"])

# Auswahl validieren
selected = model_output.get("selected", [])

if not isinstance(selected, list):
    raise ValueError("'selected' must be a list")

verified = []
invalid = []
seen = set()

for code in selected:
    if not isinstance(code, str) or code not in candidates:
        invalid.append(code)
        continue

    if code in seen:
        invalid.append(code)
        continue

    seen.add(code)

    if len(verified) >= 5:
        invalid.append(code)
        continue

    item = candidates[code]

    verified.append({
        "code": code,
        "preferredName": item["preferredName"],
        "id": item["id"],
    })

# Ergebnis speichern
report = {
    "model": MODEL,
    "method": "candidate-code selection",
    "runtime_seconds": round(duration, 1),
    "prompt_tokens": result.get("prompt_eval_count"),
    "output_tokens": result.get("eval_count"),
    "retrieved_candidates": len(candidates),
    "selected_subjects": verified,
    "invalid_codes": invalid,
}

output_path = DATA_DIR / "gnd_rag_v2_result.json"

output_path.write_text(
    json.dumps(report, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

print("\n--- AUSGEWÄHLTE GND-SCHLAGWÖRTER ---")

for subject in verified:
    print(
        f"{subject['code']} | "
        f"{subject['preferredName']} | "
        f"{subject['id']}"
    )

print("\n--- STATISTIK ---")
print(f"Laufzeit: {duration:.1f} Sekunden")
print("Prompt-Tokens:", result.get("prompt_eval_count"))
print("Output-Tokens:", result.get("eval_count"))
print("Ausgewählte Schlagwörter:", len(verified))
print("Ungültige Codes:", len(invalid))
print("Gespeichert:", output_path)

