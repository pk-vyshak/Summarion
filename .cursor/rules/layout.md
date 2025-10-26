# Project Layout

## Directory Structure

```
summarion/                   # package root
  core/
    contracts.py             # Protocol-based interfaces (ModeStrategy, Store, LLMClient)
    models.py                # Pydantic v2 schemas (Message, SummaryResult, Task, Decision...)
    pipeline.py              # Main orchestration (preprocess → summarize → persist)
    policies.py              # Token budgets, cost limits, retries, backoff
    telemetry.py             # OTEL spans, metrics, structured logging
  modes/
    __init__.py
    pointwise.py             # Mode: extract key points with attribution
    key_decisions.py         # Mode: extract decisions with rationale/owner/date
    action_items.py          # Mode: extract tasks with owner/due/priority
    timeline.py              # Mode: chronological events with timestamps
    narrative_digest.py      # Mode: freeform summary with optional quotes
    daily_digest.py          # Mode: grouped summaries by day
    registry.py              # Dynamic mode discovery/registration
    prompts/                 # Versioned prompt templates (YAML)
  llm/
    __init__.py
    base.py                  # LLMClient protocol + base class
    openai.py                # OpenAI adapter
    anthropic.py             # Anthropic adapter
    azure_openai.py          # Azure OpenAI adapter
    ollama.py                # Ollama/vLLM adapter
  stores/
    __init__.py
    base.py                  # Store protocol + base class
    memory.py                # InMemoryStore
    redis_store.py           # RedisStore
    sqlite_store.py          # SQLiteStore
    postgres_store.py        # PostgresStore
    s3_store.py              # S3JsonStore
  preprocess/
    __init__.py
    pii.py                   # PII redaction hooks (regex + pluggable NLP)
    normalize.py             # Whitespace cleanup, timestamp normalization, speaker mapping
  cli/
    __init__.py
    __main__.py              # Typer app: `summ` command
    commands.py              # Individual CLI commands
  integrations/
    langchain_example/       # LangChain integration demo
    langgraph_example/       # LangGraph integration demo
    llamaindex_example/      # LlamaIndex integration demo
  eval/
    __init__.py
    runner.py                # Eval harness
    datasets/                # Sample JSONL files
  tests/
    unit/
    integration/
    fixtures/
  docs/
    quickstart.md
    architecture.md
    extending_modes.md
```

## File Naming Conventions
- Python files: `snake_case.py`
- Test files: `test_*.py` or `*_test.py`
- Integration examples: `*_example.py` or `*/example.py`

## Module Organization
- Each major component (modes, llm, stores) has a `base.py` with protocol + abstract base
- Implementations inherit from base and are pluggable
- No circular imports: core → modes → llm/stores (one-way dependency)
