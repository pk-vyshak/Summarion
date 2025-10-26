# Testing Guidelines

## Test Structure

```
tests/
  unit/
    test_modes.py           # Test each mode strategy
    test_stores.py           # Test store implementations
    test_llm_adapters.py     # Test LLM client adapters
    test_preprocessors.py    # Test PII/normalization
    test_pipeline.py         # Test orchestration logic
  integration/
    test_end_to_end.py       # Full pipeline runs
    test_stores_integration.py  # Real Redis/SQLite/Postgres
  fixtures/
    sample_messages.jsonl    # Test conversations
    mock_llm_responses.json  # Canned LLM outputs
```

## Test Patterns

### Unit Tests (Mock External Dependencies)
```python
@pytest.fixture
def mock_openai_client(monkeypatch):
    def fake_complete(prompt, **kwargs):
        return '{"items": [...]}'
    monkeypatch.setattr(OpenAIClient, "complete", fake_complete)
    return OpenAIClient()

def test_pointwise_mode(mock_openai_client):
    strategy = PointwiseStrategy()
    messages = load_fixture("sample_messages.jsonl")
    result = strategy.summarize(messages, mock_openai_client)
    assert len(result.points) > 0
```

### Integration Tests (Real Dependencies)
```python
@pytest.mark.integration
def test_redis_store_real():
    store = RedisStore(url="redis://localhost:6379/0")
    namespace = f"test_{uuid4().hex}"
    try:
        result = SummaryResult(mode="pointwise", points=[])
        store.save_result(namespace, result)
        loaded = store.load_context(namespace)
        assert loaded["mode"] == "pointwise"
    finally:
        store.delete_namespace(namespace)
```

### Fixture Loading
```python
@pytest.fixture
def sample_messages():
    with open("tests/fixtures/sample_messages.jsonl") as f:
        return [Message(**json.loads(line)) for line in f]
```

## Coverage Targets
- Unit tests: >90% coverage
- Integration tests: Cover all stores (Redis, SQLite, Postgres)
- Mode tests: Each mode has happy path + edge cases

## Mock LLM Responses
```python
@pytest.fixture
def mock_llm_response():
    return {
        "key_decisions": '''
        {
          "decisions": [
            {
              "decision": "Use Redis for caching",
              "rationale": "Low latency",
              "owner": "alice",
              "date": "2024-01-15",
              "source_msg_ids": ["msg_1", "msg_3"]
            }
          ]
        }
        ''',
        "pointwise": '''
        {
          "points": [
            {"text": "Important point", "source_msg_ids": ["msg_1"]}
          ]
        }
        '''
    }
```

## Running Tests

```bash
# All tests
pytest

# Unit tests only
pytest tests/unit

# Integration tests only
pytest tests/integration -m integration

# Specific file
pytest tests/unit/test_modes.py

# With coverage
pytest --cov=summarion --cov-report=html
```

## Edge Cases to Test

### Mode Strategies
- Empty conversations
- Single message
- Very long conversations (chunking)
- Malformed LLM responses (JSON + regex fallback)
- Missing source_msg_ids

### Stores
- Concurrent writes to same namespace
- Namespace not found
- Large payloads (>1MB)
- Connection failures (retry logic)

### Preprocessors
- No PII detected
- Multiple PII types
- Redacted content
- Redaction report generation

## Eval Harness
```python
# eval/runner.py
def run_eval(mode: str, dataset_path: str):
    """Run mode on dataset and compute metrics."""
    dataset = load_jsonl(dataset_path)
    results = []
    for conv in dataset:
        result = summarize(conv, mode=mode)
        results.append({
            "precision": compute_precision(result, conv.labels),
            "recall": compute_recall(result, conv.labels),
            "coverage": compute_coverage(result, conv)
        })
    return export_csv(results)
```
