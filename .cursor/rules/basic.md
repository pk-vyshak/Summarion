# Cursor Rules — Enterprise Summarization + Memory Framework

## Project Compass
- Build an **enterprise-grade, open-source framework** that converts message streams into **typed, auditable summaries and durable memory**.
- First-class **modes** with versioned prompts & schemas: `pointwise`, `key_decisions`, `action_items`, `timeline`, `narrative_digest`, `daily_digest`.
- **Pluggable** LLM adapters (OpenAI/Anthropic/Azure/Ollama) and **store** adapters (InMemory/Redis/SQLite/Postgres/S3).
- We are not an agent runtime or retrieval system (v1). We integrate with LangChain/LangGraph/LlamaIndex, not replace them.

## Invariants (Never Break)
1. **Structured outputs only** via Pydantic v2 models. Every item must include `source_msg_ids`.
2. **Deterministic persistence** using `(namespace, mode, mode_version, window_hash)`.
3. **Separation of concerns**: strategies (prompts/parsers) are pure; pipeline orchestrates; stores persist.
4. **Provider-neutral**: core depends only on `LLMClient` protocol, not vendor SDKs.
5. **Security-first**: PII redaction runs **before** LLM calls; emit `redaction_report` in `metadata`.
6. **Observability**: OTEL traces + metrics for LLM calls and store ops; JSON logs via structlog.
7. **Backwards compatibility**: prompts & schemas are versioned (e.g., `key_decisions@1`).

## Tech Baseline
- Python 3.11+, Pydantic v2, mypy (strict), ruff (formatter), pytest (+pytest-asyncio), Typer (CLI), structlog, OpenTelemetry.
- Stores: Redis/SQLite (MVP), Postgres/S3 (1.0). License: Apache-2.0.