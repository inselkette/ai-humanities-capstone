# Milestone 3 — First Experiments Log
**Due: 27.11.2026**  
**Experiments run: 24.11.2026**

The records below use the prescribed experiment format. Prompt version
labels are assigned retrospectively for documentation; they were not
recorded as separate versioned prompt files at execution time.
The complete model outputs and source document are kept locally.
See [the detailed experiment log](experiment_log.md) for additional
metrics, setup, and interpretation.

---

## Experiment template

```text
### Experiment [N] — [short description]
Date: YYYY-MM-DD
Model: [model name + version]
Prompt version: [e.g. v001]
Layer: [baseline | prompted | rag | agents]

**Question asked:**
> ...

**Output:**
> ...

**What I noticed:**
-
-

**What I will change next:**
-
```

---

### Experiment 1 — Baseline summarization (4B)
Date: 2026-11-24  
Model: gemma3:4b (Ollama)  
Prompt version: baseline-v001  
Layer: baseline

**Question asked:**
> Summarize the following document in English in approximately 200 words.

The prompt included the extracted text of *Building sustainable
international partnerships as a Team Europe* (JOIN(2024) 25 final).

**Output:**
> English summary discussing Team Europe, Global Gateway,
> development financing, sustainable development, and regional
> partnerships (paraphrased here; the full output is stored locally).

Runtime: 53.9 seconds. Prompt tokens: 13,441.
Generated tokens: 316.

**What I noticed:**
- The local run completed successfully.
- The 42% global ODA figure mentioned by the model was supported by
  the source, although the model omitted its reference year (2023).
- These spot-checks do not establish the summary's overall accuracy.

**What I will change next:**
- Run the identical baseline prompt with Gemma 3 12B.

### Experiment 2 — Baseline summarization (12B)
Date: 2026-11-24  
Model: gemma3:12b (Ollama)  
Prompt version: baseline-v001  
Layer: baseline

**Question asked:**
> Summarize the following document in English in approximately 200 words.

The prompt included the same extracted document as Experiment 1.

**Output:**
> English summary emphasizing international partnerships,
> Global Gateway, private investments, and strategic cooperation
> (paraphrased here; the full output is stored locally).

Runtime: 172.1 seconds. Prompt tokens: 13,441.
Generated tokens: 299.

**What I noticed:**
- The 12B run took about 3.2 times as long as the 4B run.
- The mentioned Global Gateway target of up to EUR 300 billion by
  2027 was supported by a spot-check against the source.
- The runs alone do not establish that either model is more accurate.

**What I will change next:**
- Test structured output and evaluate document-grounded claims.

### Experiment 3 — Structured abstract and keywords
Date: 2026-11-24  
Model: gemma3:4b (Ollama)  
Prompt version: structured-v001  
Layer: prompted

**Question asked:**
> Produce an English abstract of approximately 200 words, five
> German subject keywords with reasons, and uncertainties.

The prompt included the extracted document.

**Output:**
> Free-text keywords: Entwicklungszusammenarbeit;
> Globale Partnerschaften; Nachhaltigkeit; Geopolitik;
> Investitionsstrategie.
>
> The abstract and uncertainties are stored locally.

Runtime: 67.8 seconds. Prompt tokens: 13,593.
Generated tokens: 746.

**What I noticed:**
- The keywords had not been verified against an authority file.
- Some uncertainty statements were themselves poorly supported
  by the source.

**What I will change next:**
- Use the free-text keywords to retrieve GND candidates.

### Experiment 4 — GND retrieval and model-generated labels/IDs
Date: 2026-11-24  
Model: gemma3:4b (Ollama)  
Prompt version: gnd-rag-v001  
Layer: rag

**Question asked:**
> Select up to five appropriate GND subject headings from the
> retrieved candidates and return their labels, identifiers,
> and short explanations.

The model received the full document and 22 unique GND candidate
records retrieved through lobid-gnd.

**Output:**
> Formally matching entries: Entwicklungshilfe (4014948-1),
> Entwicklungsprojekt (4070874-3),
> Kirchliche Entwicklungshilfe (4127506-8),
> Nachhaltigkeit (4326464-5).
>
> Non-matching label/identifier pair:
> Global Gateway — 1299843611.

Runtime: 56.6 seconds. Prompt tokens: 14,614.
Generated tokens: 364. Formally matching records: 4.
Invalid label/identifier pairings: 1.

**What I noticed:**
- The retrieved GND identifier 1299843611 was attached to
  Environmental, Social and Governance, not Global Gateway.
- Kirchliche Entwicklungshilfe was a formally valid record
  but appeared inappropriate as a central subject of the document.
- Formal authority validity and semantic relevance are distinct.

**What I will change next:**
- Restrict the model to internal candidate codes and let
  Python resolve labels and GND identifiers.

### Experiment 5 — GND retrieval with deterministic code mapping
Date: 2026-11-24  
Model: gemma3:4b (Ollama)  
Prompt version: gnd-rag-v002  
Layer: rag

**Question asked:**
> Select up to five subject headings using only internal
> candidate codes from the retrieved list. Return fewer
> if fewer are appropriate.

The model received the same document and the same pool of
22 candidate records.

**Output:**
> C01: Entwicklungszusammenarbeit (4198756-1)
> C04: Clean Development Mechanism (4835547-1)

Runtime: 41.6 seconds. Prompt tokens: 13,813.
Generated tokens: 19. Selected codes: 2.
Invalid codes: 0.

**What I noticed:**
- Python correctly associated each valid code with its record,
  preventing incorrect name/ID combinations within the candidate pool.
- Clean Development Mechanism appeared semantically inappropriate.
- Different prompts and output formats mean the runtime and
  selection differences are not attributable to one isolated variable.

**What I will change next:**
- Broaden candidate retrieval.
- Require evidence for each selected heading.
- Evaluate formal correctness, relevance, and topical coverage separately.

---

## Model comparison notes

The observations concern these individual summarization runs,
not a general ranking of the models.

| Model | Strength observed | Weakness observed |
|-------|-------------------|-------------------|
| Gemma 3 4B | Faster baseline run (53.9 s); included quantitative ODA detail | Omitted the reference year for the 42% ODA figure; factual completeness not systematically assessed |
| Gemma 3 12B | Discussed strategic partnerships and the verified Global Gateway investment target | Slower baseline run (172.1 s); no demonstrated overall accuracy advantage |

The two baseline runs used an identical prompt. For the broader
methodological discussion and caveats, see [experiment_log.md](experiment_log.md).
