
from pathlib import Path
import requests
import time

text = Path(
    "data/processed/eu_partnerships.txt"
).read_text(encoding="utf-8")

prompt = f"""
You are assisting with subject indexing and abstracting
of public-sector documents for an academic library.

Analyze the following document.

Produce:

1. ABSTRACT
Write an objective English abstract of approximately
200 words. Describe the purpose, principal themes,
policy measures, and conclusions of the document.

2. SUBJECT KEYWORDS
Suggest exactly five subject keywords in German,
suitable for indexing in an academic library.

For each keyword, provide a brief explanation
of its relevance to the document.

Do not claim that these keywords are verified GND
headings. GND verification will be performed separately.

3. UNCERTAINTIES
Identify any information that could not be
established reliably from the document.

Use only information supported by the document.
Do not invent facts, references, or identifiers.

DOCUMENT:
{text}
"""

model = "gemma3:4b"

print(f"Starte {model} mit strukturiertem Prompt ...")

start = time.time()

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0,
            "num_ctx": 16384,
            "num_predict": 900
        }
    },
    timeout=600
)

response.raise_for_status()
result = response.json()

output = Path("data/processed/gemma4b_structured.txt")
output.write_text(result["response"], encoding="utf-8")

print("\n", result["response"])
print("\nLaufzeit:", round(time.time() - start, 1), "s")
print("Prompt-Tokens:", result.get("prompt_eval_count"))
print("Output-Tokens:", result.get("eval_count"))
print("Ergebnis:", output)

