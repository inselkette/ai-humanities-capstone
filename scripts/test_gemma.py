
from pathlib import Path
import requests
import time

# Dokument laden
text = Path(
    "data/processed/eu_partnerships.txt"
).read_text(encoding="utf-8")

# Einfacher Baseline-Prompt
prompt = f"""
Summarize the following document in English
in approximately 200 words.

DOCUMENT:
{text}
"""

print("Starte Gemma 3 4B ...")

start = time.time()

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "gemma3:4b",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0,
            "num_ctx": 16384,
            "num_predict": 600
        }
    },
    timeout=600
)

response.raise_for_status()
result = response.json()

duration = time.time() - start
summary = result["response"]

# Ergebnis speichern
output = Path("data/processed/gemma4b_baseline.txt")
output.write_text(summary, encoding="utf-8")

print("\n--- ZUSAMMENFASSUNG ---\n")
print(summary)
print(f"\nLaufzeit: {duration:.1f} Sekunden")
print(f"Ergebnis gespeichert: {output}")
print("Prompt-Tokens:", result.get("prompt_eval_count"))
print("Output-Tokens:", result.get("eval_count"))

