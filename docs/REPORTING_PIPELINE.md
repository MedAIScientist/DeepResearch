# Reporting Pipeline

Eye of Prometheus separates *research* from *report generation* to balance accuracy and narrative quality.

## Stage 1 — Research Brief (Tongyi DeepResearch)

- Implemented in `eye_of_prometheus.ask.run_research`.
- Relies on Alibaba Tongyi DeepResearch 30B via OpenRouter.
- Produces an evidence-rich Markdown snapshot with:
  - The original question
  - Tool outputs (search + visit transcripts)
  - Model reasoning enclosed in `<answer>...</answer>` tags
  - Metadata (model name, rollout index, timestamps)

The brief is saved to `outputs/reports/report_<timestamp>.md` and is intentionally concise to remain within context limits.

## Stage 2 — Executive Report (xAI grok-4-fast)

- Unleashed through `report_generator.generate_comprehensive_report`.
- Default model is `x-ai/grok-4-fast` (2M-token context). Override via `REPORT_MODEL`.
- Receives the research brief and the question, then produces an 8k+ word English report with:
  - Executive summary
  - Thematic chapters
  - Tables, bullet lists, and inline citations
  - Implications, risk analysis, and future outlook

The output is stored at `outputs/reports/comprehensive_report_<timestamp>_<slug>.md` with YAML front matter for easy publishing.

## Prompt Design Highlights

- **Language enforcement:** System prompts insist on English-only responses to avoid unexpected translations.
- **Structure cues:** Markdown headings and required sections are listed to keep reports predictable.
- **Depth controls:** Word-count targets, paragraph length expectations, and instructions to add examples prevent shallow outputs.
- **Token safety:** `REPORT_CONTEXT_LIMIT` (default 2M tokens) and `REPORT_MAX_TOKENS` (default 800k) ensure the request stays within the model's context window.

## Offline Regeneration

The `synthesize_only.py` script reuses the Stage 2 prompt so you can experiment with alternative synthesis instructions without recomputing research facts. It pulls the latest chunk outputs, estimates token usage, and emits a new Markdown report.

