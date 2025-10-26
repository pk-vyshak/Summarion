# Anti-Patterns & What NOT to Do

## ❌ Architecture Violations

### Don't: Tight Coupling
```python
# BAD: Direct import of vendor SDK in core
from openai import OpenAI

# GOOD: Use protocol interface
from llm.base import LLMClient

class Summarizer:
    def __init__(self, llm: LLMClient):
        self.llm = llm
```

### Don't: Skip Attribution
```python
# BAD: No source_msg_ids
class Point(BaseModel):
    text: str

# GOOD: Always track attribution
class Point(BaseModel):
    text: str
    source_msg_ids: List[str]
```

### Don't: Side Effects in Strategies
```python
# BAD: Mode strategy modifies global state
class MyMode:
    def parse(self, text):
        global_cache["last_mode"] = self.name  # NO!

# GOOD: Pure functions only
class MyMode:
    def parse(self, text):
        return parsed_data  # No side effects
```

## ❌ Security Anti-Patterns

### Don't: Log Sensitive Data
```python
# BAD: Log full message content
logger.info("messages", messages=raw_messages)

# GOOD: Log IDs/metadata only
logger.info("messages", count=len(messages), ids=[m.id for m in messages])
```

### Don't: Skip PII Redaction
```python
# BAD: Send to LLM without redaction
self.llm.complete(redacted_prompt)  # if redaction not applied!

# GOOD: Always redact first
redacted = self.preprocessors.redact_pii(messages)
self.llm.complete(self.strategy.prompt(redacted))
```

### Don't: Hardcode Secrets
```python
# BAD: Secrets in code
api_key = "sk-abc123"

# GOOD: Environment variables
api_key = os.getenv("OPENAI_API_KEY")
```

## ❌ Error Handling Anti-Patterns

### Don't: Silent Failures
```python
# BAD: Ignore errors
try:
    result = strategy.parse(text)
except:
    pass  # NO!

# GOOD: Log and raise
try:
    result = strategy.parse(text)
except ParseError as e:
    logger.error("parse_failed", mode=strategy.name, error=str(e))
    raise
```

### Don't: Broad except
```python
# BAD: Catch all exceptions
except Exception:
    pass

# GOOD: Catch specific exceptions
except (JSONDecodeError, ValidationError) as e:
    logger.warning("fallback_parsing", error=str(e))
    return self._regex_parse(text)
```

## ❌ Performance Anti-Patterns

### Don't: Block on Stores
```python
# BAD: Synchronous blocking call
results = store.load_context(namespace)  # blocks

# GOOD: Async or timeout
async def load_async():
    return await store.load_context_async(namespace)

# Or with timeout
with timeout(5):
    results = store.load_context(namespace)
```

### Don't: No Token Budgets
```python
# BAD: No limits
self.llm.complete(prompt)  # Could be huge!

# GOOD: Enforce limits
self.policies.enforce_token_budget(prompt)
self.llm.complete(prompt, max_tokens=self.policies.max_tokens)
```

## ❌ Observability Anti-Patterns

### Don't: Unstructured Logs
```python
# BAD: Print statements
print(f"Summarizing {len(messages)} messages")

# GOOD: Structured logging
logger.info("summarizing", message_count=len(messages))
```

### Don't: No Metrics
```python
# BAD: No telemetry
result = self.llm.complete(prompt)

# GOOD: Track everything
with self.telemetry.span("llm_call"):
    result = self.llm.complete(prompt)
    self.telemetry.record_tokens(tokens)
    self.telemetry.record_cost(cost)
```

## ❌ Code Quality Anti-Patterns

### Don't: Ignore Type Hints
```python
# BAD: No types
def summarize(messages):
    ...

# GOOD: Full type annotations
def summarize(messages: List[Message]) -> SummaryResult:
    ...
```

### Don't: Duplicate Code
```python
# BAD: Copy-paste prompt logic
class ModeA:
    def prompt(self):
        return f"System: {sys_prompt} User: {user_prompt}"

class ModeB:
    def prompt(self):
        return f"System: {sys_prompt} User: {user_prompt}"  # Duplicate!

# GOOD: Shared base class
class BaseMode:
    def prompt(self):
        return f"{self.system_prompt}\n\n{self.user_prompt}"

class ModeA(BaseMode):
    system_prompt = "..."
    user_prompt = "..."
```

### Don't: Magic Strings
```python
# BAD: Hardcoded strings
if mode == "key_decisions":
    ...

# GOOD: Constants
from modes.registry import MODES
from modes.key_decisions import KEY_DECISIONS

if mode == KEY_DECISIONS.name:
    ...
```

## ❌ Documentation Anti-Patterns

### Don't: Missing Docstrings
```python
# BAD: No docs
def parse(text):
    return json.loads(text)

# GOOD: Docstrings + type hints
def parse(text: str) -> SummaryResult:
    """Parse LLM output into typed schema.
    
    Args:
        text: Raw JSON string from LLM
        
    Returns:
        SummaryResult with parsed data
        
    Raises:
        JSONDecodeError: If text is not valid JSON
        ValidationError: If schema is invalid
    """
    return SummaryResult(**json.loads(text))
```

## ✅ Remember
- **Always** include `source_msg_ids`
- **Never** log sensitive data
- **Always** use protocols/interfaces
- **Never** skip error handling
- **Always** add telemetry
- **Never** break backwards compatibility
