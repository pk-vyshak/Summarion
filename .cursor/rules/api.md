# Public API Guidelines

## SDK API Design

### Entry Point: Summarizer
```python
from summarion import Summarizer, RedisStore, OpenAIClient, Policies

# Construct
summ = Summarizer(
    store=RedisStore(url="redis://localhost:6379/0"),
    llm=OpenAIClient(model="gpt-4o-mini"),
    policies=Policies(
        max_tokens=4000,
        max_cost_usd=0.05,
        retry_backoff_seconds=[1, 2, 5]
    )
)

# Use
result = summ.summarize(
    messages=messages,
    mode="key_decisions",
    namespace="chat:acme:proj1",
    options={"max_decisions": 8}
)
```

### Store Interface
```python
# Stores are pluggable
from summarion.stores import RedisStore, SQLiteStore, PostgresStore

redis_store = RedisStore(
    url="redis://localhost:6379/0",
    namespace="default"
)

sqlite_store = SQLiteStore(
    db_path="./summaries.db"
)

postgres_store = PostgresStore(
    connection_string="postgresql://...",
    schema="summaries"
)

summ = Summarizer(store=redis_store)
```

### LLM Adapter Interface
```python
from summarion.llm import OpenAIClient, AnthropicClient, AzureOpenAIClient

# OpenAI
openai_client = OpenAIClient(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

# Anthropic
anthropic_client = AnthropicClient(
    model="claude-3-sonnet-20240229"
)

# Azure
azure_client = AzureOpenAIClient(
    endpoint="https://...",
    deployment_name="gpt-4"
)

summ = Summarizer(llm=azure_client)
```

## CLI API Design

### Basic Usage
```bash
# From JSONL file
summ summarize \
  --mode key_decisions \
  --in messages.jsonl \
  --out decisions.json

# From stdin
cat messages.jsonl | summ summarize --mode pointwise --out - > output.json

# With store
summ summarize \
  --mode key_decisions \
  --in messages.jsonl \
  --store redis://localhost:6379/0?ns=chat:acme \
  --out decisions.json
```

### Options
```bash
# Specify model
summ summarize --mode pointwise --in messages.jsonl --model openai:gpt-4o-mini

# Cost budget
summ summarize --mode pointwise --in messages.jsonl --max-cost-usd 0.10

# Token limit
summ summarize --mode pointwise --in messages.jsonl --max-tokens 8000

# PII redaction
summ summarize --mode pointwise --in messages.jsonl --enable-pii-redaction

# Namespace
summ summarize --mode pointwise --in messages.jsonl --namespace chat:prod:sales
```

### Mode-Specific Options
```bash
# Key decisions: limit number
summ summarize --mode key_decisions --in messages.jsonl --max-decisions 10

# Action items: only high priority
summ summarize --mode action_items --in messages.jsonl --min-priority high

# Timeline: date range
summ summarize --mode timeline --in messages.jsonl --start-date 2024-01-01
```

## Python SDK Examples

### Basic Summarization
```python
from summarion import Summarizer, MemoryStore, OpenAIClient

summ = Summarizer(
    store=MemoryStore(),
    llm=OpenAIClient(model="gpt-4o-mini")
)

messages = [
    Message(id="1", role="user", content="Let's use Redis"),
    Message(id="2", role="assistant", content="Good choice for caching")
]

result = summ.summarize(messages, mode="pointwise")
print(result.points)
```

### Hierarchical Memory
```python
# Rolling summary
rolling = summ.summarize(
    messages=last_100_messages,
    mode="pointwise",
    namespace="session_123",
    memory_level="rolling"
)

# Session summary
session = summ.summarize(
    messages=all_session_messages,
    mode="narrative_digest",
    namespace="session_123",
    memory_level="session"
)
```

### Custom LLM Configuration
```python
from summarion.llm import OpenAIClient

custom_llm = OpenAIClient(
    model="gpt-4o",
    temperature=0.3,
    max_tokens=8000,
    timeout=30
)

summ = Summarizer(llm=custom_llm)
```

### Error Handling
```python
from summarion import SummarizeError

try:
    result = summ.summarize(messages, mode="key_decisions")
except SummarizeError as e:
    logger.error(f"Failed: {e}")
    # Handle error
```

## Context Loading
```python
# Load previous context
context = summ.store.load_context(
    namespace="chat:acme:proj1",
    mode="key_decisions"
)

# Incremental summary
result = summ.summarize(
    messages=new_messages,
    mode="key_decisions",
    namespace="chat:acme:proj1",
    context=context
)
```

## Telemetry Access
```python
# Access metrics after summarize call
result, telemetry = summ.summarize_with_telemetry(messages, mode="pointwise")

print(f"Tokens: {telemetry.tokens_used}")
print(f"Cost: ${telemetry.cost_usd}")
print(f"Latency: {telemetry.latency_ms}ms")
```

## Namespacing
```python
# Multi-tenant via namespaces
result_acme = summ.summarize(
    messages, mode="key_decisions",
    namespace="chat:acme:proj1"
)

result_beta = summ.summarize(
    messages, mode="key_decisions",
    namespace="chat:beta:proj1"
)

# Load by namespace
acme_decisions = summ.store.load_context("chat:acme:proj1")
```

## Versioned Modes
```python
# Explicit version
result = summ.summarize(
    messages, 
    mode="key_decisions@1"  # Pin to specific version
)

# Latest version (default)
result = summ.summarize(
    messages,
    mode="key_decisions"  # Always uses latest
)
```
