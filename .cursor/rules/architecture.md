# Architecture Principles

## Pipeline Flow
```
Messages (JSONL/List[Message])
  ↓
Preprocessors (PII redaction, normalization)
  ↓
Chunker/Windowing (sliding windows for large conversations)
  ↓
ModeStrategy (generate prompt + output schema)
  ↓
LLM Adapter (call provider API)
  ↓
Parser (JSON-first; retry with regex fallback)
  ↓
Post-process (deduplicate, validate attribution)
  ↓
Memory Manager (rolling/hierarchical summaries)
  ↓
Store Adapter (persist to Redis/SQLite/Postgres/S3)
  ↓
Telemetry (metrics, logs, traces)
```

## Core Components

### ModeStrategy
- **Single Responsibility**: Generate prompts and parse outputs
- **Stateless**: No side effects, pure functions
- **Versioned**: `mode@version` (e.g., `key_decisions@1`)
- **Testable**: Prompt templates live in YAML

### LLMClient
- **Provider-agnostic**: Protocol interface only
- **Configurable**: model, temperature, max_tokens via kwargs
- **Observable**: Log tokens, cost, latency for every call
- **Resilient**: Retry on rate limits, timeouts

### Store
- **Namespace isolation**: Multi-tenant via `namespace` parameter
- **Audit trail**: Append-only logs + current snapshot
- **Context loading**: Load prior summaries for hierarchical memory
- **Configurable**: Connection strings via env vars

### Pipeline
- **Orchestration only**: Delegates to strategies/adapters
- **Policy enforcement**: Token budgets, cost limits, retries
- **Telemetry integration**: Spans, metrics, logs
- **Error recovery**: Graceful degradation

## Memory Model

### Hierarchical Summaries
1. **Rolling**: Last N messages → rolling summary
2. **Session**: All messages in session → session summary
3. **Canonical**: Periodically refresh full history → canonical summary

### Attribution
- Every bullet/decision includes `source_msg_ids`
- Traces back to original messages
- Supports drill-down in UI

### Deterministic Hashes
```python
window_hash = hashlib.sha256(
    mode + mode_version + str(message_ids_sorted)
).hexdigest()
```

## Security Model
- **PII redaction**: Run before LLM calls (configurable patterns)
- **Namespace isolation**: Store-level access control
- **Encryption**: Store-specific (optional at-rest encryption)
- **Audit logs**: All operations logged with namespace + user

## Observability
- **OTEL spans**: Each LLM call, store op, mode execution
- **Metrics**: tokens, cost_usd, latency_ms, failures, retries
- **Logs**: Structured JSON via structlog
- **Exports**: Prometheus, StatsD, or custom collectors
