# Summarion

![CI](https://github.com/summarion/summarion/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)

An enterprise-grade, open-source Summarization + Memory Framework for building intelligent summarization systems.

## Overview

Summarion is a flexible, production-ready framework for processing and summarizing conversational data (meetings, support chats, product discussions, legal reviews, etc.) with built-in memory management, auditability, and observability.

## Key Features

- **Multiple Summarization Modes**: Pointwise, key decisions, action items, timelines, narrative digests, and more
- **Flexible LLM Adapters**: OpenAI, Anthropic, Azure OpenAI, Ollama/vLLM support
- **Persistent Memory**: Multiple storage backends (in-memory, Redis, SQLite, Postgres, S3)
- **Hierarchical Memory**: Rolling, session, and canonical memory levels
- **Enterprise Features**: PII redaction, audit trails, cost tracking, telemetry
- **Production Ready**: Comprehensive testing, CI/CD, documentation

## Status

🚧 This project is in active development. Version 1.0 roadmap available in [tasks.md](tasks.md).

## Installation

```bash
# Coming soon: pip install summarion
```

## Quick Start

```python
from summarion import Summarizer, InMemoryStore
from summarion.llm import OpenAIClient

store = InMemoryStore()
llm = OpenAIClient(api_key="...")
summarizer = Summarizer(store=store, llm_client=llm)

messages = [...]  # Your conversation messages

result = summarizer.summarize(
    messages=messages,
    mode="pointwise",
    namespace="project-alpha"
)

print(result.summary)
```

## Architecture

- **Core Contracts**: Protocol-based design for modes, LLMs, and stores
- **Pipeline Orchestration**: Preprocessing → chunking → mode execution → LLM → parsing → storage
- **Policies**: Token budgets, cost limits, retry logic, latency budgets
- **Telemetry**: Structured logging, OpenTelemetry traces, Prometheus metrics

## Development

```bash
# Set up development environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"

# Run tests
pytest

# Lint and format
ruff check .
ruff format .

# Type checking
mypy .
```

## Contributing

Contributions are welcome! Please check [tasks.md](tasks.md) for active development areas.

## License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.

## Roadmap

- Week 0-3: MVP with core modes, stores, and LLM adapters
- Week 4-5: Enterprise features (auditability, hierarchical memory, PII redaction, observability)
- Week 6-7: Additional modes, stores, LLM adapters, eval harness
- Week 8-9: Documentation, integrations, security hardening, versioning
- Week 10+: Advanced enterprise features

