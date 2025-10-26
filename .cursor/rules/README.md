# Cursor Rules Overview

This directory contains development guidelines for the **Enterprise Summarization + Memory Framework**.

## Files

- **[basic.md](./basic.md)** - Project compass, invariants, and tech baseline
- **[layout.md](./layout.md)** - Directory structure and file organization
- **[architecture.md](./architecture.md)** - Pipeline flow, core components, memory model
- **[patterns.md](./patterns.md)** - Code patterns, conventions, best practices
- **[modes.md](./modes.md)** - Guide for developing new summarization modes
- **[testing.md](./testing.md)** - Testing structure, patterns, coverage targets
- **[api.md](./api.md)** - Public SDK and CLI API design
- **[do-not.md](./do-not.md)** - Anti-patterns and what to avoid

## Quick Reference

### Core Principles
- **Attribution**: Every output item MUST include `source_msg_ids`
- **Structured**: Pydantic v2 models for all data
- **Pluggable**: Protocol-based design (no vendor lock-in)
- **Auditable**: Deterministic hashes, append-only logs
- **Secure**: PII redaction before LLM calls
- **Observable**: OTEL traces, structured logs, metrics

### Architecture
```
Messages → Preprocessors → Chunker → ModeStrategy → LLMClient → 
Parser → Post-process → MemoryManager → StoreAdapter → Telemetry
```

### Adding a Mode
1. Create `modes/your_mode.py` implementing `ModeStrategy`
2. Add prompt in `modes/prompts/your_mode.yaml`
3. Define schema in `core/models.py`
4. Write tests in `tests/unit/modes/test_your_mode.py`
5. Register in `modes/registry.py`

### Testing
- Unit tests: >90% coverage with mocked dependencies
- Integration tests: Real Redis/SQLite/Postgres stores
- Eval harness: Precision/recall vs human labels

### Never Do
- ❌ Skip `source_msg_ids` attribution
- ❌ Log sensitive data
- ❌ Tight coupling to vendor SDKs
- ❌ Side effects in strategies
- ❌ Silent failures
- ❌ Magic strings

### Always Do
- ✅ Protocol-based interfaces
- ✅ PII redaction before LLM
- ✅ Structured logging
- ✅ Telemetry on all operations
- ✅ Type hints everywhere
- ✅ Backwards compatibility
