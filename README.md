# Gazzali Research

**Repository:** [https://github.com/MedAIScientist/DeepResearch](https://github.com/MedAIScientist/DeepResearch)

**Gazzali Research** is an academic-focused AI research assistant named after Al-Ghazali (1058-1111), the renowned Islamic philosopher, theologian, and scholar. This command-line tool orchestrates Alibaba Cloud's **Tongyi DeepResearch 30B** agent for scholarly investigations and **xAI's grok-4-fast** model for academic report synthesis. The system provides specialized features for academic research including citation management, literature review synthesis, methodology analysis, and peer-review quality outputs.

<div align="center">
<img src="https://github.com/alicankiraz1/Eye-of-Prometheus/blob/main/PoC.gif" width="800">
</div>

## Key Capabilities

- **Academic-focused research** — Prioritize peer-reviewed sources, scholarly databases, and academic publications for credible research.
- **Citation management** — Automatic citation tracking and formatting in APA, MLA, Chicago, and IEEE styles with bibliography generation.
- **Literature review synthesis** — Systematic analysis of existing research with gap identification and thematic organization.
- **Methodology analysis** — Extract and document research methodologies, study designs, and analytical techniques from papers.
- **Chunked investigation pipeline** — Break complex research questions into focused sub-questions for comprehensive coverage.
- **Academic report generation** — Generate structured reports following academic conventions with proper sections and formal writing style.
- **Research question refinement** — Transform broad topics into specific, answerable research questions using FINER criteria.
- **Offline synthesis utility** — Re-run synthesis on existing research outputs without repeating the costly research phase.

## Project Layout

```text
Gazzali-Research/
├── install.sh                 # Bootstrap script (venv, requirements, .env provisioning)
├── requirements.txt           # Python dependencies
├── .env.example               # Template for API credentials
├── scripts/
│   └── ask.sh                 # CLI wrapper that activates the virtualenv and runs the tool
├── src/
│   └── gazzali/
│       ├── __init__.py        # Package init + env loader
│       ├── config.py          # Configuration and environment helpers
│       ├── ask.py             # Interactive CLI entrypoint
│       ├── chunked_research.py# Chunked research orchestration
│       ├── report_generator.py# Academic report synthesis logic
│       ├── synthesize_only.py # Offline synthesis command
│       └── DeepResearch/      # Alibaba Tongyi DeepResearch agent
└── docs/
    ├── CHUNKED_WORKFLOW.md    # Chunked research flow documentation
    └── REPORTING_PIPELINE.md  # Two-stage reporting architecture
```

## External Services & References

| Provider | Purpose | Reference |
|----------|---------|-----------|
| [OpenRouter](https://openrouter.ai) | Unified gateway for Tongyi DeepResearch and grok-4-fast | [OpenRouter docs](https://openrouter.ai/docs) |
| [Alibaba Tongyi DeepResearch 30B](https://openrouter.ai/api/v1/models/alibaba/tongyi-deepresearch-30b-a3b) | Autonomous research agent | [Technical report](https://arxiv.org/pdf/2510.24701) |
| [xAI grok-4-fast](https://openrouter.ai/api/v1/models/x-ai/grok-4-fast) | Fast reasoning/synthesis model | [Model announcement](https://x.ai/) |
| [Serper.dev](https://serper.dev) | Google Search/Scholar API wrapper | [Documentation](https://serper.dev/api-documentation) |
| [Jina AI Reader](https://jina.ai/reader) | Web content extraction and Markdown conversion | [API docs](https://jina.ai/reader/) |

## Prerequisites

- macOS/Linux with Python 3.10–3.13 (`python3 -m venv` required)
- OpenRouter API key with access to Tongyi DeepResearch and grok-4-fast
- Serper.dev API key for Google Search/Scholar
- Jina AI Reader API key for webpage summarisation

> ⚠️ **Costs & Rate Limits:** Tongyi DeepResearch and grok-4-fast both rely on billable OpenRouter calls. Large chunked runs and synthesis outputs may consume significant tokens; monitor your plan usage carefully.

## Installation

```bash
git clone https://github.com/MedAIScientist/DeepResearch.git
cd DeepResearch
./install.sh
```

The installer will:

1. Create `.venv` in the project root.
2. Upgrade `pip` and install dependencies from `requirements.txt`.
3. Prompt for OpenRouter, Serper, and Jina API keys.
4. Generate `.env` with the provided credentials.

At any time you can re-run the script to reinstall dependencies (existing `.env` files will be preserved).

## Quick Start

### Standard Research Mode

```bash
source .venv/bin/activate
export PYTHONPATH="$(pwd)/src:$PYTHONPATH"
python -m gazzali.gazzali "What are the most significant AI safety milestones announced in 2024?"
```

Or, with the convenience wrapper:

```bash
./scripts/gazzali.sh "What are the most significant AI safety milestones announced in 2024?"
```

### Academic Research Mode

For scholarly research with enhanced features:

```bash
# Academic paper with APA citations
./scripts/gazzali.sh --academic --citation-style apa "Impact of AI on education"

# Literature review in social sciences
./scripts/gazzali.sh --academic --output-format review --discipline social \
    "Social media effects on mental health"

# Research proposal with question refinement
./scripts/gazzali.sh --academic --output-format proposal --refine \
    "Climate change adaptation strategies"
```

The academic mode provides:
- **Citation management** — Automatic tracking and formatting in APA, MLA, Chicago, or IEEE
- **Scholar priority** — Prioritizes Google Scholar over general web search
- **Structured sections** — Abstract, Introduction, Literature Review, Methodology, etc.
- **Discipline-specific conventions** — Tailored terminology and writing style for STEM, social sciences, humanities, or medical fields
- **Bibliography export** — Generate .bib files for reference managers

### Legacy CLI (ask.py)

The original CLI is still available for backward compatibility:

```bash
./scripts/ask.sh "What are the most significant AI safety milestones announced in 2024?"
```

`./scripts/ask.sh` and `./scripts/gazzali.sh` automatically set `PYTHONPATH` to include `src/`, so you can invoke them without exporting the variable manually. When launching the module yourself, be sure `src/` is present on `PYTHONPATH` as shown above.

The CLI will:

1. Validate environment variables and show masked API keys.
2. Create a JSONL dataset for the DeepResearch agent.
3. Invoke `DeepResearch/inference/run_multi_react.py` via OpenRouter.
4. Display the immediate research findings (in English, with tool citations).
5. Save a Markdown research brief under `outputs/reports/`.
6. Call grok-4-fast (2M context) to produce an extended executive report (~8k+ words) and store it in the same directory.

### Chunked Research Mode

For expansive topics, enable chunking so the system decomposes the question and synthesises the combined evidence:

```bash
./scripts/ask.sh --chunked "Map the global regulation landscape for frontier AI systems"
```

This mode:

1. Uses OpenRouter `gpt-4o-mini` to propose 3–7 sub-questions.
2. Runs DeepResearch sequentially for each chunk (new dataset per sub-question).
3. Stores chunk results under `outputs/openrouter-api/...`.
4. Calls grok-4-fast with all chunk summaries to craft a single integrated report.

### Offline Synthesis

If you already collected chunk outputs but want a new synthesis pass (e.g., with updated prompts), run:

```bash
python -m gazzali.synthesize_only "Original research question here"
```

The utility locates the most recent chunk run, reloads its JSONL outputs, and regenerates an English synthesis report without re-hitting the search APIs.

## CLI Reference

### Main CLI (gazzali.py)

The new `gazzali.py` CLI provides both standard and academic research modes:

```bash
python -m gazzali.gazzali [OPTIONS] [QUESTION]
```

**Academic Mode Options:**
- `--academic` — Enable academic research mode
- `--citation-style {apa,mla,chicago,ieee}` — Citation format (default: apa)
- `--output-format {paper,review,proposal,abstract,presentation}` — Document format (default: paper)
- `--discipline {general,stem,social,humanities,medical}` — Academic discipline (default: general)
- `--refine` — Refine research question using FINER criteria
- `--word-count COUNT` — Target word count (default: 8000)
- `--export-bib` — Export bibliography to .bib file

**General Options:**
- `--chunked` — Enable chunked research mode
- `--no-keep` — Do not keep temporary dataset files
- `--output-dir PATH` — Custom output directory

For detailed CLI documentation, see [docs/CLI_INTERFACE.md](docs/CLI_INTERFACE.md).

## Configuration & Environment Variables

`src/gazzali/config.py` automatically loads `.env` from the project root. The following keys are recognised:

| Variable | Description |
|----------|-------------|
| `OPENROUTER_API_KEY` | Required. OpenRouter API key (must start with `sk-or-`). |
| `SERPER_API_KEY` | Optional but recommended. Enables Google Search/Scholar tooling. |
| `JINA_API_KEY` | Optional but recommended. Powers the `visit` tool for webpage extraction. |
| `MODEL_PATH` | Leave empty when using OpenRouter (defaults to `openrouter-api`). |
| `OUTPUT_PATH` | Override output directory; defaults to `<project>/outputs`. |
| `TEMPERATURE`, `PRESENCE_PENALTY`, `MAX_WORKERS`, `ROLLOUT_COUNT` | Advanced agent tuning parameters. |
| `OPENROUTER_MAX_RETRIES` | Upper bound for retry attempts when a call fails (default: 3). |
| `OPENROUTER_TIMEOUT` | Per-request timeout in seconds for OpenRouter calls (default: 180). |
| `OPENROUTER_RETRY_BASE` | Initial backoff delay in seconds for retry logic (default: 0.5). |
| `OPENROUTER_RETRY_MAX_SLEEP` | Maximum sleep between retries in seconds (default: 6). |
| `REPORT_MODEL` | Reporting model for synthesis (default: `x-ai/grok-4-fast`). |
| `REPORT_CONTEXT_LIMIT` | Approximate total context window to target (default: 2000000 tokens). |
| `REPORT_MAX_TOKENS` | Cap on output tokens for synthesis (default: 800000). |
| **Academic Mode Settings** | |
| `CITATION_STYLE` | Default citation style: apa, mla, chicago, ieee (default: apa). |
| `OUTPUT_FORMAT` | Default output format: paper, review, proposal, abstract, presentation (default: paper). |
| `DISCIPLINE` | Default discipline: general, stem, social, humanities, medical (default: general). |
| `WORD_COUNT_TARGET` | Target word count for academic reports (default: 8000). |
| `SCHOLAR_PRIORITY` | Prioritize Scholar tool over general search (default: true). |
| `EXPORT_BIBLIOGRAPHY` | Export bibliography to .bib file (default: false). |
| `MIN_PEER_REVIEWED_SOURCES` | Minimum peer-reviewed sources required (default: 5). |
| `SOURCE_QUALITY_THRESHOLD` | Minimum source quality score 0-10 (default: 7). |

All Python modules access configuration via `gazzali.get_env`, ensuring `.env` values are respected without manual wiring.

## Docs & Deep Dives

- `docs/CHUNKED_WORKFLOW.md` — How decomposition, per-chunk processing, and synthesis interlock.
- `docs/REPORTING_PIPELINE.md` — Detailed explanation of the two-stage reporting flow (research vs. synthesis, prompt design, token budgeting).

## Troubleshooting

- **Missing dependencies**: Re-run `./install.sh` to recreate the virtual environment and reinstall packages.
- **API errors**: Ensure your OpenRouter plan includes both Tongyi DeepResearch and grok-4-fast. Check account quotas.
- **SERPER / Jina warnings**: The CLI allows execution without these keys, but search/visit calls will be skipped or degraded.
- **Large outputs**: grok-4-fast supports an ~2M-token context; chunked synthesis dynamically caps requested tokens to stay under model limits.

## Credits

- **Alibaba-NLP** for [Tongyi DeepResearch](https://github.com/Alibaba-NLP/DeepResearch) (bundled under `src/gazzali/DeepResearch`).
- **xAI** for [grok-4-fast](https://x.ai/).
- **OpenRouter**, **Serper.dev**, and **Jina AI** for their APIs.

This repository repackages open-source components to provide an opinionated, English-first research workflow. Review upstream licenses before redistribution.

