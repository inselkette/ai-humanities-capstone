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
