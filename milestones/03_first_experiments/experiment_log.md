# Milestone 3 — First Experiments

**Date:** 24 November 2026
**Deadline:** 27 November 2026
**Status:** In progress

## 1. Research objective

These exploratory experiments investigate how model size, prompt design,
and retrieval of GND authority records affect summarization and
subject indexing of public-sector documents.

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

Baseline summarization parameters:
- Temperature: 0
- Context window: 16,384 tokens
- Maximum generated tokens: 600
- Streaming: disabled

The structured and GND experiments used different prompts and output
limits. Their results are therefore not directly comparable as
controlled tests of model size alone.

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

The PDF text was successfully processed by both Gemma 3 4B and 12B.
The 4B model also produced a structured abstract and free-text keywords.
Subsequent retrieval experiments tested candidate selection against GND
authority data. Sections 8 and 9 report the measurements and errors.

## 6. Current limitations

- Experiments use only one document and are exploratory.
- There is no human-annotated reference summary or indexing gold standard.
- Factual verification consists of limited source spot-checks.
- Subject-heading appropriateness has been assessed qualitatively.
- GND v1 and v2 use different prompts and output formats.
- Runs have not been independently repeated for stability assessment.
- Effective context use and possible input truncation need verification.
- Retrieved candidate records may be incomplete or irrelevant.

## 7. Next steps after Milestone 3

1. Expand the evaluation to multiple public-sector documents.
2. Establish human-reviewed reference summaries and subject headings.
3. Improve GND candidate retrieval and inspect source-text evidence.
4. Measure formal validity, semantic relevance, and topical coverage separately.
5. Repeat runs to assess robustness and effective context usage.
6. Develop and evaluate a working prototype.

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

## 10. Milestone 3 submission summary (27 November 2026)

This milestone demonstrates a reproducible exploratory workflow for
AI-assisted discovery of public-sector documents. A 19-page European
Commission / High Representative document was extracted with PyMuPDF
and processed locally through Ollama.

Two Gemma 3 model sizes (4B and 12B) were compared using the same
baseline summarization prompt. The 4B run took 53.9 seconds, while
the 12B run took 172.1 seconds. A limited check against the source
confirmed two quantitative claims, but did not establish overall
factual accuracy or superiority of either model.

A structured 4B experiment generated an abstract and five free-text
German keywords. These keywords were then used to retrieve 22
unique GND candidate records through lobid-gnd. In the first
retrieval-augmented selection experiment, the model produced four
formally matching records and one mismatched label/identifier pair.
In the second experiment, Python assigned authority metadata from
model-selected candidate codes; both selected codes mapped correctly,
although one heading appeared semantically inappropriate.

The principal finding is that authority-record retrieval and
deterministic identifier mapping can improve formal consistency,
but do not by themselves ensure meaningful subject indexing.
Future work will focus on better candidate retrieval, evidence-based
selection, and human-reviewed evaluation.

The experiments are documented in this log and their Python scripts
are stored in the repository. The source PDF, extracted text, and
model output files remain local and are excluded from version control.

## 11. Planned extension: University of Vienna u:ai API comparison

**Status: Planned, not yet executed (24 November 2026).**

The University of Vienna u:ai API account has been activated and its
model-list endpoint queried successfully. This provides an opportunity
to compare locally run Gemma 3 models with externally hosted models
on the same public-sector document.

**Initial candidates:**
- `gpt-5-mini` (University of Vienna u:ai API)
- `gemini-3.5-flash` (University of Vienna u:ai API)

**Proposed procedure:**
1. Confirm the API request schema and permitted data use in the
   University's official documentation.
2. Reuse the extracted text of JOIN(2024) 25 final and the identical
   approximately 200-word English baseline summarization instruction.
3. Record the exact model identifiers, date, prompt, settings,
   latency, token usage, cost if reported, and full output locally.
4. Evaluate factual accuracy and omissions using the source text and
   the questions in `src/evaluation/questions.md`.
5. If feasible, run the structured abstract/keyword prompt and
   GND candidate-selection workflow with the same candidate pool.
6. Report model/provider differences as exploratory findings, without
   claiming a controlled comparison where settings differ.

**Important limitations and safeguards:** API-hosted models may differ
in tokenization, default reasoning settings, safety configuration,
and cost accounting. These are potential confounders. Never commit
the client ID, client secret, or any credential-bearing request to
GitHub. Only public, rights-cleared documents should be sent to the
external API. The model-list response indicates available model IDs,
not measured performance.

**University documentation:**
https://zid.univie.ac.at/uai/uai-api-zugang

This is follow-up work and is not required for the already documented
Milestone 3 experiments.
