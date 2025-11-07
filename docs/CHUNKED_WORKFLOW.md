# Chunked Research Workflow

The chunked pipeline handles questions that are too broad for a single research run by decomposing them into smaller, tractable prompts. The flow is implemented in `src/eye_of_prometheus/chunked_research.py` and is exposed through the CLI (`python -m eye_of_prometheus.ask --chunked ...`).

## High-level Stages

1. **Decomposition**
   - Uses `openai/gpt-4o-mini` through OpenRouter to propose 3–7 sub-questions.
   - Results are logged to the console so you can see how the problem is being partitioned.

2. **Per-chunk research**
   - For each generated sub-question the CLI writes a dedicated JSONL dataset under `DeepResearch/inference/eval_data`.
   - `run_multi_react.py` is invoked with Tongyi DeepResearch 30B via OpenRouter.
   - Output JSONL files are written beneath `outputs/openrouter-api/.../iter1.jsonl`.

3. **Synthesis**
   - Chunk results are aggregated into a Markdown payload (`## Sub-Question N: ...`).
   - The configured synthesis model (default: x-ai/grok-4-fast) receives the combined context and produces an English mega-report (~8k+ words).

```
┌───────────────┐    ┌────────────────────┐    ┌────────────────────┐    ┌────────────────────────────┐
│ User question │ →  │ Decompose question │ →  │ Run DeepResearch    │ →  │ Synthesize with grok-4-fast │
└───────────────┘    └────────────────────┘    └────────────────────┘    └────────────────────────────┘
```

## Token Budgeting

The synthesis stage estimates usage with `len(combined_results) // 4` tokens. Defaults are `REPORT_CONTEXT_LIMIT=2000000` and `REPORT_MAX_TOKENS=800000`, which you can adjust in `.env` to match the capabilities of the model you select. If the buffer becomes too small, reduce the number of chunks or refine the decomposition prompt.

## Tips

- If decomposition fails (e.g., due to network issues), the pipeline automatically falls back to a single research run.
- You can edit `chunked_research.decompose_question` to change the model or instructions used for planning.
- Clean up old chunk runs in `outputs/` periodically to keep the repository tidy.

