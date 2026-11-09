# Milestone 2 — Material and Ethics Note
**Due: 13 November 2026**

## Your collection

### What is it?
The project, *Beyond Full Text: AI-Assisted Discovery of Public Sector Documents*, will investigate the technical quality of LLM-generated summaries of European Commission evaluation reports on international partnerships and development cooperation. The principal research question is: **How can different LLM-based summarization approaches improve the accuracy, completeness, and usefulness of summaries of public-sector documents?**

The pilot corpus will consist of five candidate evaluation reports, selected for different topics and document lengths. The longer-term target is approximately 20–30 reports, subject to feasibility and rights review.

### Where does it come from?
The documents are published in the European Commission's Directorate-General for International Partnerships (DG INTPA) publications library. Candidate records, **not yet downloaded, individually rights-checked, or technically inspected**, are:

1. **Evaluation of ADELANTE (final / ex-post phase 1 and interim second phase)** (29 October 2024): https://international-partnerships.ec.europa.eu/publications-library/evaluation-adelante-final-ex-post-phase-1-and-interim-second-phase_en
2. **Evaluation of Contribution to the Implementation of the Sustainable Development Goals by EU External Action in the Period 2016–2021** (8 March 2024): https://international-partnerships.ec.europa.eu/publications-library/evaluation-contribution-implementation-sustainable-development-goals-eu-external-action-period-2016_en
3. **Final evaluation of the China–EU School of Law programme** (31 December 2024): https://international-partnerships.ec.europa.eu/publications-library/final-evaluation-china-eu-school-law-programme_en
4. **Mid-term review of PROMOVE Agribiz** (1 August 2024): https://international-partnerships.ec.europa.eu/publications-library/mid-term-review-promove-agribiz_en
5. **Evaluation of Farm Enterprise Development through Inputs and Services (FEDIS)** (27 August 2024): https://international-partnerships.ec.europa.eu/publications-library/evaluation-farm-enterprise-development-through-inputs-and-services-fedis_en

For each selected PDF, a source inventory will record its title, URL, publication date, issuing institution, named authors or contractors where available, licence statement, any third-party material, download date, and processing status.

### How will you prepare it?
1. Download only reports for which the intended processing is appropriate after a document-level rights and sensitivity check.
2. Extract text from PDF files using Python; record extraction failures and use OCR only where necessary and appropriate.
3. Remove repeated headers and footers, check reading order, and preserve section boundaries and page references where possible.
4. Prepare both full-text inputs (where model context limits permit) and section-level chunks for retrieval.
5. Generate a simple baseline summary, compare versioned structured prompts, and implement a RAG-based approach with source references.
6. Compare outputs using the same documents and 5–10 fixed evaluation questions. Assess factual support, coverage of key findings, relevance, coherence, and traceability. Include human review of a manageable sample.

Raw PDFs and extracted text will be stored locally rather than committed to the public repository until publication rights and any sensitive content have been reviewed.

### Size and scope
Initial pilot: **five candidate reports**, with final inclusion dependent on rights and extraction checks. Planned extension: **approximately 20–30 reports**. Exact page counts, word counts, and file sizes have not yet been measured.

---

## Ethical considerations

### Copyright and licensing
The European Commission's general reuse policy permits reuse of EU-owned content under CC BY 4.0 unless otherwise indicated, with attribution and indication of changes. This general notice **does not establish the licence or third-party rights status of each selected evaluation report**. Individual PDF notices, contractor contributions, figures, photographs, and other third-party content will be checked before processing or publishing outputs.

Official general policy: https://european-union.europa.eu/legal-notice_en

This capstone focuses on **technical summary quality**, not a legal determination of whether AI-generated summaries of restricted documents may be published. The project's longer-term library discovery use case will require separate legal review. No conclusion of legal compliance is claimed.

### Consent
These are institutional publications rather than material collected directly from participants for this project. However, reports may include interviews, quotations, or identifiable individuals. The pilot will review such content before submission to external model APIs and avoid transmitting unnecessary personal or sensitive data. Public availability alone is not treated as consent for every secondary use.

### Whose voices are present?
The corpus primarily reflects the European Commission's evaluation framework and the perspectives included by report authors and evaluators. Some reports may include implementing partners, government officials, and programme participants; representation will be assessed document by document.

### Whose voices are absent or marginalised?
People affected by development interventions, local civil-society groups, and dissenting perspectives may be underrepresented or filtered through institutional reporting practices. A summary can further erase nuance or uncertainty; this will be considered during qualitative evaluation.

### Limits you will communicate to users
- AI summaries may omit key qualifications or misstate findings and must not replace the source documents.
- Generated claims need verification against the report; citations are evidence pointers, not automatic proof of correctness.
- Retrieval may miss relevant sections, and a RAG system is not inherently more accurate than a full-document approach.
- Outputs reflect the limitations and biases of the source corpus and the model.
- Summaries will be marked as AI-generated, linked to source records, and subject to human review before public release.
- Copyright, confidentiality, and personal-data questions remain subject to document-specific assessment and, for the longer-term application, legal review.

## Planned next steps
- Verify the five candidate PDFs, individual copyright notices, and text extractability.
- Record bibliographic and rights metadata in `docs/data_sources.md`.
- Prepare a fixed evaluation set and a human-review rubric.
- Run the baseline, structured-prompt, and RAG approaches on the approved pilot corpus.
