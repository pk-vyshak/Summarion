# Enterprise Summarization + Memory Framework - Tasks Roadmap

## Overview

This document tracks the implementation roadmap for building an enterprise-grade, open-source Summarization + Memory Framework. Tasks are organized by milestone weeks, with detailed breakdowns for immediate work (Weeks 0-3) and higher-level tasks for later phases.

**How to use this file:**
- Check off tasks as they're completed (mark with ✅)
- Add notes/comments after completing tasks
- Update estimates if tasks take longer/shorter than expected
- Mark dependencies when blocked

---

## Week 0-1: Foundations

**Goal:** Set up project infrastructure, define core contracts, establish CI/CD

### Repository Setup
- [x] Initialize Git repository
- [x] Choose and set project name (e.g., `summarion`)
- [x] Add Apache-2.0 LICENSE file
- [x] Add `.gitignore` for Python/IDE files
- [x] Create README.md with project overview
- [x] Initialize Python package structure (`summarion/` directory)

### Code Quality & CI
- [x] Set up `pyproject.toml` with dependencies (pydantic>=2.0, structlog, opentelemetry, etc.)
- [x] Configure `ruff` for linting and formatting
- [x] Configure `mypy` for type checking (strict mode)
- [x] Add `pytest` and `pytest-asyncio` for testing
- [x] Set up pre-commit hooks (ruff, mypy, pytest on staged files)
- [x] Create GitHub Actions CI workflow (run tests on push/PR)
- [x] Add badge to README (tests passing, license)

### Core Contracts (Protocols)
- [x] Create `core/__init__.py`
- [x] Create `core/contracts.py` with:
  - [x] `ModeStrategy` protocol (prompt, parse methods)
  - [x] `LLMClient` protocol (complete method)
  - [x] `Store` protocol (load_context, save_result, append_log)
  - [x] Base classes for each protocol
- [x] Create `core/models.py` with Pydantic models:
  - [x] `Message` (id, role, content, ts)
  - [x] `SummaryResult` (mode, title, points, decisions, timeline, summary, metadata)
  - [x] `AttributedPoint` (text, source_msg_ids)
  - [x] `Decision` (decision, rationale, owner, date, source_msg_ids)
  - [x] `Task` (task, owner, due, priority, source_msg_ids)
  - [x] `Event` (timestamp, event, source_msg_ids)

### Skeleton Structure
- [ ] Create directory structure: `modes/`, `llm/`, `stores/`, `preprocess/`, `cli/`, `integrations/`, `eval/`, `docs/`
- [ ] Add `__init__.py` files to all directories
- [ ] Create placeholder `modes/registry.py`
- [ ] Create placeholder `cli/__main__.py` with Typer setup
- [ ] Create placeholder `eval/runner.py`

**Estimated:** 20-30 hours

---

## Week 2-3: MVP Core

**Goal:** Build working end-to-end with 2 modes, 2 LLM adapters, 3 stores, and CLI

### Modes Implementation
- [ ] Create `modes/base.py` with base ModeStrategy class
- [ ] Implement `modes/pointwise.py`:
  - [ ] Create prompt template in `modes/prompts/pointwise.yaml`
  - [ ] Implement prompt() method
  - [ ] Implement parse() method (JSON-first, regex fallback)
  - [ ] Add unit tests in `tests/unit/modes/test_pointwise.py`
- [ ] Implement `modes/key_decisions.py`:
  - [ ] Create prompt template in `modes/prompts/key_decisions.yaml`
  - [ ] Implement prompt() method
  - [ ] Implement parse() method (JSON-first, regex fallback)
  - [ ] Add unit tests in `tests/unit/modes/test_key_decisions.py`
- [ ] Update `modes/registry.py` to register both modes

### LLM Adapters
- [ ] Create `llm/base.py` with LLMClient base class
- [ ] Implement `llm/openai.py`:
  - [ ] Complete method with OpenAI SDK
  - [ ] Error handling for rate limits
  - [ ] Timeout configuration
  - [ ] Add unit tests with mocked responses
- [ ] Implement `llm/anthropic.py`:
  - [ ] Complete method with Anthropic SDK
  - [ ] Error handling for rate limits
  - [ ] Timeout configuration
  - [ ] Add unit tests with mocked responses

### Store Implementations
- [ ] Create `stores/base.py` with Store base class
- [ ] Implement `stores/memory.py` (InMemoryStore):
  - [ ] Load/save/append methods
  - [ ] Namespace isolation
  - [ ] Add unit tests
- [ ] Implement `stores/redis_store.py`:
  - [ ] Connect to Redis
  - [ ] Load/save/append methods
  - [ ] Namespace isolation
  - [ ] Connection pooling
  - [ ] Add integration tests (requires Redis)
- [ ] Implement `stores/sqlite_store.py`:
  - [ ] Create SQLite database schema
  - [ ] Load/save/append methods
  - [ ] Namespace isolation
  - [ ] Add integration tests

### Pipeline & Orchestration
- [ ] Create `core/pipeline.py`:
  - [ ] Summarizer main class
  - [ ] Orchestrate: preprocess → chunk → mode → llm → parse → post-process → store
  - [ ] Error handling and logging
  - [ ] Context loading for hierarchical summaries
- [ ] Create `core/policies.py`:
  - [ ] Token budget enforcement
  - [ ] Cost limit checking
  - [ ] Retry logic with backoff
- [ ] Create `core/telemetry.py`:
  - [ ] Basic structured logging with structlog
  - [ ] Metrics stub (tokens, cost, latency)

### CLI
- [ ] Implement `cli/commands.py` with commands:
  - [ ] `summarize` command (main)
  - [ ] Options: --mode, --in, --out, --store, --model
  - [ ] Options: --max-tokens, --max-cost-usd
  - [ ] Options: --namespace, --enable-pii-redaction
- [ ] Update `cli/__main__.py` to use Typer CLI
- [ ] Add CLI tests with typer.testing

### End-to-End Examples
- [ ] Create `tests/fixtures/sample_messages.jsonl`:
  - [ ] Sample meeting transcript
  - [ ] Sample support chat
  - [ ] Sample product discussion
- [ ] Create integration test: `tests/integration/test_e2e.py`
  - [ ] Test with MemoryStore
  - [ ] Test with RedisStore
  - [ ] Test with SQLiteStore
  - [ ] Verify output JSON structure

**Estimated:** 60-80 hours

---

## Week 4-5: Enterprise Spine

**Goal:** Add auditability, hierarchical memory, policies, PII redaction, observability

### Auditability
- [ ] Update all modes to always include `source_msg_ids`
- [ ] Add deterministic hash generation (window_hash based on mode + messages)
- [ ] Implement append-only change log in stores:
  - [ ] Add `log_changes()` method to Store protocol
  - [ ] Update RedisStore to log changes
  - [ ] Update SQLiteStore to log changes
  - [ ] Update MemoryStore to log changes
- [ ] Add snapshot IDs to SummaryResult

### Hierarchical Memory
- [ ] Define memory levels: rolling, session, canonical
- [ ] Add `memory_level` parameter to `Summarizer.summarize()`
- [ ] Implement windowing logic in pipeline:
  - [ ] Rolling: last N messages (configurable)
  - [ ] Session: all messages in current session
  - [ ] Canonical: periodic refresh
- [ ] Update stores to support memory level storage
- [ ] Add context merging logic

### Policies
- [ ] Extend `core/policies.py`:
  - [ ] Token budget per operation
  - [ ] Cost limits per operation
  - [ ] Latency budgets
  - [ ] Retry configurations (exponential backoff)
  - [ ] Enforce policies in pipeline
- [ ] Add policy validation on Summarizer init

### PII Redaction
- [ ] Create `preprocess/pii.py`:
  - [ ] Regex patterns for emails, phone numbers, SSN, credit cards
  - [ ] Configurable patterns (on/off per type)
  - [ ] Redaction report generation
- [ ] Create `preprocess/normalize.py`:
  - [ ] Whitespace cleanup
  - [ ] Timestamp normalization
  - [ ] Speaker mapping
- [ ] Integrate preprocessors into pipeline
- [ ] Add `redaction_report` to SummaryResult metadata
- [ ] Add unit tests for PII redaction

### Observability
- [ ] Extend `core/telemetry.py`:
  - [ ] OpenTelemetry spans for LLM calls
  - [ ] OpenTelemetry spans for store operations
  - [ ] Metrics: tokens_used, cost_usd, latency_ms, failures, retries
  - [ ] Prometheus-friendly export
- [ ] Add structured logging throughout:
  - [ ] Pipeline orchestration
  - [ ] Mode execution
  - [ ] LLM calls
  - [ ] Store operations
- [ ] Add telemetry export configuration

### Testing
- [ ] Add integration tests for hierarchical memory
- [ ] Add integration tests for PII redaction
- [ ] Add integration tests for policies (budget enforcement)
- [ ] Add telemetry tests (verify spans/metrics are emitted)

**Estimated:** 50-70 hours

---

## Week 6-7: Breadth & Stability

**Goal:** Add more modes, more stores, more LLM adapters, eval harness

### Additional Modes
- [ ] Implement `modes/action_items.py`:
  - [ ] Prompt template
  - [ ] Parser
  - [ ] Tests
- [ ] Implement `modes/timeline.py`:
  - [ ] Prompt template
  - [ ] Parser
  - [ ] Tests
- [ ] Implement `modes/narrative_digest.py`:
  - [ ] Prompt template
  - [ ] Parser
  - [ ] Tests
- [ ] Implement `modes/daily_digest.py`:
  - [ ] Prompt template
  - [ ] Parser
  - [ ] Tests

### Additional Stores
- [ ] Implement `stores/postgres_store.py`:
  - [ ] Schema design
  - [ ] Load/save/append methods
  - [ ] Connection pooling
  - [ ] Migration support
  - [ ] Integration tests
- [ ] Implement `stores/s3_store.py`:
  - [ ] S3 bucket operations
  - [ ] JSON storage format
  - [ ] Load/save/append methods
  - [ ] Integration tests

### Additional LLM Adapters
- [ ] Implement `llm/azure_openai.py`:
  - [ ] Azure-specific configuration
  - [ ] Endpoint/deployment setup
  - [ ] Tests
- [ ] Implement `llm/ollama.py`:
  - [ ] Local Ollama integration
  - [ ] vLLM support
  - [ ] Tests

### Eval Harness
- [ ] Create `eval/datasets/` directory:
  - [ ] Sample meetings dataset
  - [ ] Sample support chats dataset
  - [ ] Sample legal reviews dataset
  - [ ] Sample product discussions dataset
- [ ] Implement `eval/runner.py`:
  - [ ] Load datasets (JSONL format)
  - [ ] Run modes on datasets
  - [ ] Compute metrics (precision, recall, coverage)
  - [ ] Export results to CSV
- [ ] Add basic benchmarking:
  - [ ] Latency benchmarks
  - [ ] Token cost benchmarks
  - [ ] Drift detection (compare outputs over time)

### Stability
- [ ] Add retry logic for all LLM adapters
- [ ] Add circuit breaker for store failures
- [ ] Add validation for all inputs (messages, configs)
- [ ] Improve error messages with context
- [ ] Add integration tests for all new modes
- [ ] Test mode versioning support

**Estimated:** 60-80 hours

---

## Week 8-9: 1.0 Harden

**Goal:** Documentation, integration examples, security hardening, versioning

### Documentation
- [ ] Create `docs/quickstart.md` (5-minute guide)
- [ ] Create `docs/architecture.md` (system design)
- [ ] Create `docs/extending_modes.md` (how to add modes)
- [ ] Create `docs/api_reference.md` (SDK/CLI reference)
- [ ] Add docstrings to all public APIs
- [ ] Set up MkDocs or Sphinx
- [ ] Deploy docs site (GitHub Pages or ReadTheDocs)

### Integration Examples
- [ ] Create `integrations/langchain_example/`:
  - [ ] Working example code
  - [ ] README with instructions
- [ ] Create `integrations/langgraph_example/`:
  - [ ] Working example code
  - [ ] README with instructions
- [ ] Create `integrations/llamaindex_example/`:
  - [ ] Working example code
  - [ ] README with instructions
- [ ] Add Slack integration example (transcript → summary)
- [ ] Add Meet integration example (transcript → summary)

### Security
- [ ] Add config encryption support (optional)
- [ ] Document redaction policies (what's redacted by default)
- [ ] Add role-based ACLs for stores (namespace-level)
- [ ] Security audit checklist
- [ ] Add security best practices to docs

### Versioning
- [ ] Implement prompt/schema versioning:
  - [ ] Support `mode@version` syntax
  - [ ] Parse version from mode string
  - [ ] Load correct version of prompt
  - [ ] Validate schema version
- [ ] Add deprecation policy (N+2 versions supported)
- [ ] Add deprecation warnings for old versions
- [ ] Version all existing modes as `@1`

### Release Preparation
- [ ] Write CHANGELOG.md
- [ ] Create v1.0.0 release notes
- [ ] Tag release in Git
- [ ] Publish to PyPI
- [ ] Announce release

**Estimated:** 50-70 hours

---

## Week 10+: Enterprise Features

**Goal:** Advanced features for enterprise deployments

### Multi-Tenant Enhancements
- [ ] SSO (OIDC) integration for admin UI (if UI added)
- [ ] Enhanced namespace isolation
- [ ] Tenant-level quota management
- [ ] Resource limits per namespace

### Policy Packs
- [ ] Define compliance presets (HIPAA, GDPR, SOC2)
- [ ] Implement policy pack loading
- [ ] Auto-configure redaction based on pack
- [ ] Add policy pack documentation

### Dataset-Level Guardrails
- [ ] Define dataset schemas
- [ ] Enforce schema validation
- [ ] Dataset-level access controls
- [ ] Audit dataset access

### Background Workers
- [ ] Add async worker support
- [ ] Kafka integration for streaming summaries
- [ ] Queue-based incremental refresh
- [ ] Scheduled summary generation

### Advanced Observability
- [ ] Custom metric dashboards
- [ ] Alerting on failures
- [ ] Distributed tracing
- [ ] Cost analytics

**Estimated:** 80-100 hours (ongoing)

---

## Quick Reference

### Dependencies
- **Protocols**: All implementations depend on `core/contracts.py`
- **Models**: All code depends on `core/models.py`
- **Pipeline**: Uses `core/pipeline.py`, `core/policies.py`, `core/telemetry.py`
- **Modes**: Depend on contracts and models, use `llm/` adapters
- **CLI**: Depends on pipeline and all adapters
- **Integrations**: Depend on main SDK

### Tech Stack
- Python 3.11+
- Pydantic v2
- structlog for logging
- OpenTelemetry for traces
- Typer for CLI
- pytest for testing
- ruff + mypy for quality

### Key Files to Create
- `core/contracts.py` - Protocols
- `core/models.py` - Pydantic schemas
- `core/pipeline.py` - Main orchestration
- `modes/` - Mode implementations
- `llm/` - LLM adapters
- `stores/` - Store adapters
- `cli/__main__.py` - CLI entry point

### Documentation Links
- `.cursor/rules/README.md` - Overview of all rules
- `.cursor/rules/architecture.md` - Architecture principles
- `.cursor/rules/modes.md` - How to add modes
- `.cursor/rules/api.md` - API design guidelines

---

## Progress Tracking

**Current Status:** Week 0 - Not Started

**Overall Progress:** 0% (0/XXX tasks complete)

**Week-by-Week Targets:**
- Week 0-1: Foundations ⏳
- Week 2-3: MVP Core ⏳
- Week 4-5: Enterprise Spine ⏳
- Week 6-7: Breadth & Stability ⏳
- Week 8-9: 1.0 Harden ⏳
- Week 10+: Enterprise Features ⏳

---

## Notes

Add your notes here as you work through tasks. For example:

- API key management approach
- Testing environment setup
- Performance benchmarks
- Issues encountered and resolutions
