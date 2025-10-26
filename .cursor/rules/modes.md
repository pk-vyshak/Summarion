# Mode Development Guide

## Adding a New Mode

1. **Create mode file** in `modes/your_mode.py`
2. **Implement ModeStrategy protocol**
3. **Add prompt template** in `modes/prompts/your_mode.yaml`
4. **Define output schema** in `core/models.py`
5. **Add tests** in `tests/unit/modes/test_your_mode.py`
6. **Register** in `modes/registry.py`

## Mode Implementation Template

```python
from typing import List, Dict, Any
from core.contracts import ModeStrategy
from core.models import Message, SummaryResult

class YourModeStrategy(ModeStrategy):
    """Description of what this mode extracts."""
    
    name = "your_mode"
    version = "1"
    
    def __init__(self):
        self.prompt_template = self._load_prompt("your_mode")
    
    def prompt(self, messages: List[Message], opts: Dict[str, Any]) -> str:
        """Generate system + user prompt."""
        system_prompt = self.prompt_template["system"]
        user_prompt = self.prompt_template["user"].format(
            messages=self._format_messages(messages),
            max_items=opts.get("max_items", 10)
        )
        return f"{system_prompt}\n\n{user_prompt}"
    
    def parse(self, raw_text: str) -> SummaryResult:
        """Parse LLM output into SummaryResult."""
        # Try JSON first
        try:
            data = json.loads(raw_text)
            return SummaryResult(
                mode=self.name,
                **self._validate_schema(data)
            )
        except json.JSONDecodeError:
            # Fallback to regex parsing
            return self._regex_parse(raw_text)
    
    def _validate_schema(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate parsed data against expected schema."""
        # Use Pydantic to validate
        ...
```

## Prompt Template Format

Create `modes/prompts/your_mode.yaml`:

```yaml
version: "1"
system: |
  You are a specialized AI that extracts [specific information] from conversations.
  
  Instructions:
  - Return valid JSON only
  - Include source_msg_ids for each item
  - Be concise and accurate

user: |
  Extract [specific information] from the following conversation.
  Maximum: {max_items} items.
  
  Conversation:
  {messages}
  
  Respond with JSON:
  {{
    "items": [
      {{
        "text": "...",
        "source_msg_ids": ["msg_1", "msg_2"]
      }}
    ]
  }}
```

## Required Schema Attributes

Every mode output MUST include:
- `mode: str` - the mode name
- `source_msg_ids: List[str]` - attribution links
- `metadata: Dict[str, Any]` - extra context (optional)

## Mode-Specific Schemas

Define in `core/models.py`:

```python
class YourModeOutput(BaseModel):
    """Schema for your_mode output items."""
    text: str
    source_msg_ids: List[str]
    # add mode-specific fields
```

Then in `SummaryResult`:
```python
class SummaryResult(BaseModel):
    mode: str
    # ... common fields ...
    your_mode_items: List[YourModeOutput] = []  # add field
```

## Testing Your Mode

```python
def test_your_mode_parses_correctly():
    strategy = YourModeStrategy()
    messages = [Message(id="1", role="user", content="test")]
    
    # Mock LLM response
    raw = '{"items": [...]}'
    result = strategy.parse(raw)
    
    assert result.mode == "your_mode"
    assert len(result.your_mode_items) > 0
    assert all("msg_1" in item.source_msg_ids for item in result.your_mode_items)
```

## Eval Recipe

Add to `eval/runner.py`:
- Load sample conversations
- Run your mode
- Compare extracted items vs human labels
- Compute precision/recall/coverage

## Deprecation Policy
- Version prompts in YAML: `your_mode@1`, `your_mode@2`
- Support N+2 versions (current + 2 prior)
- Log warning when using deprecated version
