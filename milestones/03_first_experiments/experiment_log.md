# Milestone 3 — First Experiments

**Date:** 24 November 2026
**Deadline:** 27 November 2026
**Status:** In progress

## 1. Research objective

This experiment investigates how model size and prompt design
affect the quality of LLM-generated summaries of public-sector
documents.

## 2. Test document

Title: Building sustainable international partnerships as a Team Europe

Institution: European Commission / High Representative
Document identifier: JOIN(2024) 25 final
Publication date: 2 October 2024

- PDF pages: 19
- Extracted words: 7,927
- Extracted characters: 62,073
- Extraction library: PyMuPDF
- Extraction setting: sort=True

The PDF and extracted text are stored locally and excluded
from the public GitHub repository.

## 3. Experimental setup

Hardware: MacBook Air M4, 16 GB unified memory
Inference software: Ollama

Models:
- gemma3:4b
- gemma3:12b

Generation parameters:
- Temperature: 0
- Context window: 16,384 tokens
- Maximum generated tokens: 600
- Streaming: disabled

## 4. Experiment 1 — Baseline summarization

Model: gemma3:4b

Prompt instruction:
"Summarize the following document in English
in approximately 200 words."

Results:
- Execution time: 53.9 seconds
- Prompt tokens: 13,441
- Generated tokens: 316
- Execution: successful

The summary discusses Team Europe, Global Gateway,
development financing, sustainable development goals,
and regional partnerships.

These observations do not yet establish factual accuracy.

## 5. Preliminary observations

The extracted document was processed without an API error.

The model produced a coherent English summary covering
several major themes.

Factual accuracy, completeness, omissions, and unsupported
claims have not yet been systematically evaluated.

## 6. Limitations

- Only one model and one prompt have been tested.
- Only one document has been processed.
- No human reference summary has been established.
- The experiment has not yet been independently repeated.
- Model-specific tokenization and effective context usage
  require further verification.

## 7. Next steps

1. Run the identical baseline with Gemma 3 12B.
2. Design two additional prompt variants.
3. Compare outputs against the source document.
4. Document factual errors, omissions, and hallucinations.
5. Expand the experiment to additional documents.
6. Evaluate the suitability of RAG for longer documents.

## 8. Baseline comparison: Gemma 3 4B vs. 12B

Both models successfully summarized the same EU document
using identical prompts and generation parameters.

| Metric | Gemma 3 4B | Gemma 3 12B |
|---|---:|---:|
| Runtime | 53.9 s | 172.1 s |
| Prompt tokens | 13,441 | 13,441 |
| Output tokens | 316 | 299 |

The 12B model required approximately 3.2 times the runtime
of the 4B model.

### Preliminary factual verification

The following statements were checked against the extracted
source document:

1. EU and Member States accounted for 42% of global ODA
   in 2023 (source lines 60–61).
2. Global Gateway aims to mobilise up to EUR 300 billion
   in public and private investments by 2027
   (source lines 122–124).

Both statements are supported by the source.

The 4B model omitted the reference year (2023) when
reporting the ODA figure.

These findings represent a limited factual spot-check,
not a comprehensive hallucination assessment.

### Preliminary interpretation

The 4B model included more quantitative detail,
while the 12B model placed greater emphasis on strategic
relationships and private investment.

Whether the larger model provides greater factual accuracy
or completeness remains an open research question.


## 9. Structured subject indexing and GND retrieval (24 November 2026)

### Structured output with Gemma 3 4B

A structured prompt requested an English abstract, five German free-text
subject keywords, and uncertainty statements.

- Runtime: 67.8 seconds
- Prompt tokens: 13,593
- Output tokens: 746
- Free-text keywords: Entwicklungszusammenarbeit, Globale Partnerschaften,
  Nachhaltigkeit, Geopolitik, Investitionsstrategie

These keywords were not initially validated against an authority file.
Some model-generated uncertainty statements were themselves poorly
supported by the source document.

### GND candidate retrieval

The five free-text keywords were queried against the lobid-gnd API.
The revised search applied a SubjectHeading filter and returned
22 unique candidates. The results included relevant and irrelevant
authority headings, while the query "Globale Partnerschaften" returned
no candidates in the observed run.

### Experiment: GND RAG v1

The model received the document and retrieved GND candidate records.
It generated subject labels, GND identifiers, and brief justifications.

- Model: gemma3:4b
- Runtime: 56.6 seconds
- Prompt tokens: 14,614
- Output tokens: 364
- Retrieved candidates: 22
- Formally validated subject records: 4
- Invalid label/identifier pairings: 1

Formally validated output:

- Entwicklungshilfe — https://d-nb.info/gnd/4014948-1
- Entwicklungsprojekt — https://d-nb.info/gnd/4070874-3
- Kirchliche Entwicklungshilfe — https://d-nb.info/gnd/4127506-8
- Nachhaltigkeit — https://d-nb.info/gnd/4326464-5

The model also generated "Global Gateway" with identifier
https://d-nb.info/gnd/1299843611. In the retrieved candidate list,
this identifier was associated with "Environmental, Social and Governance",
not "Global Gateway". This was an incorrect label/identifier pairing,
rather than an entirely invented identifier.

"Kirchliche Entwicklungshilfe" passed the formal candidate check
but appeared semantically inappropriate for the document. Its
justification invoked religious organizations without establishing
that they were a central subject of the source.

### Experiment: GND RAG v2

The second implementation provided internally numbered candidate
codes to the model. The model returned codes only; Python then mapped
valid codes to their authority labels and identifiers.

- Model: gemma3:4b
- Runtime: 41.6 seconds
- Prompt tokens: 13,813
- Output tokens: 19
- Retrieved candidates: 22
- Selected records: 2
- Invalid codes: 0

Selected output:

- Entwicklungszusammenarbeit — https://d-nb.info/gnd/4198756-1
- Clean Development Mechanism — https://d-nb.info/gnd/4835547-1

The deterministic mapping prevented mismatched names and identifiers
within the candidate pool. However, "Clean Development Mechanism"
appeared semantically unsuitable: the specific Kyoto Protocol
mechanism had not been identified as a central topic of the document.

### Interpretation and limitations

These experiments distinguish (1) formal authority-data validity,
(2) semantic appropriateness, and (3) topical coverage. Retrieval
alone does not ensure appropriate indexing. Candidate-code selection
addresses one formal error mode but cannot guarantee relevance.

Both runs used a single document and the same initial candidate pool.
Their prompts and output formats differed, so runtime and selection
differences cannot be attributed to one isolated variable. No
human-annotated gold standard or systematic subject-indexing quality
metric has yet been established.

The next iteration should broaden candidate retrieval, consider
corporate-body records separately, and require evidence from the
source document for each selected heading.

Note: Sections 6 and 7 above describe the earlier state of the
project; subsequent experiments are documented in sections 8 and 9.
