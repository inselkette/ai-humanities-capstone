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
