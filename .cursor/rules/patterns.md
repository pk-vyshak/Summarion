# Code Patterns & Conventions

## Protocol-Based Design
```python
# Always define protocols first, then implementations
from typing import Protocol

class ModeStrategy(Protocol):
    name: str
    version: str
    
    def prompt(self, messages: List[Message], opts: Dict[str, Any]) -> str:
        """Generate system + user prompt."""
        ...
    
    def parse(self, raw_text: str) -> SummaryResult:
        """Parse LLM output into typed schema."""
        ...
```

## Pydantic Models
- Use Pydantic v2 models for all data structures
- Always include `source_msg_ids: List[str]` for attribution
- Use `Optional[...]` for nullable fields
- Add `Field(description="...")` for important fields

```python
class AttributedPoint(BaseModel):
    text: str
    source_msg_ids: List[str] = Field(
        default_factory=list,
        description="Message IDs that contributed to this point"
    )
```

## Error Handling
- Use custom exceptions with context
- Retry LLM calls with exponential backoff
- Log structured errors with `structlog`
- Always emit telemetry on failures

```python
class LLMParseError(Exception):
    """Raised when LLM output cannot be parsed."""
    def __init__(self, mode: str, raw: str, original: Exception):
        self.mode = mode
        self.raw = raw
        self.original = original
        super().__init__(f"Failed to parse {mode} output")
```

## Structured Logging
```python
logger = structlog.get_logger()

logger.info(
    "summarizing_messages",
    mode=result.mode,
    message_count=len(messages),
    token_usage=telemetry.tokens_used,
    latency_ms=telemetry.latency_ms
)
```

## Configuration
- Use environment variables for secrets (never commit)
- Use dataclasses/Pydantic for typed config
- Support TOML/YAML config files for complex setups

```python
from pydantic import BaseModel, Field

class SummarizerConfig(BaseModel):
    namespace: str
    llm_provider: str = "openai"
    max_tokens: int = 4000
    max_cost_usd: float = 0.05
```

## Testing
- Unit tests for each mode strategy, parser, store
- Integration tests with mocked LLM responses
- Use pytest fixtures for common setups
- Test with actual JSONL files in `eval/datasets/`
