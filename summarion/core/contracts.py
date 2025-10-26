"""
Protocol definitions for the summarization framework.

This module contains the core contracts (protocols) that all implementations
must adhere to. These include:
- ModeStrategy: for summarization modes
- LLMClient: for LLM provider adapters
- Store: for persistence backends
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from typing_extensions import Protocol, runtime_checkable

from summarion.core.models import Message, SummaryResult


@runtime_checkable
class ModeStrategy(Protocol):
    """Protocol for summarization modes.

    A mode is responsible for:
    1. Generating prompts from messages
    2. Parsing LLM outputs into structured results
    """

    mode_name: str
    mode_version: str

    @abstractmethod
    def prompt(self, messages: List[Message]) -> str:
        """Generate a prompt from a list of messages.

        Args:
            messages: List of messages to summarize

        Returns:
            Prompt string to send to LLM
        """

    @abstractmethod
    def parse(self, output: str, messages: List[Message]) -> SummaryResult:
        """Parse LLM output into structured summary.

        Args:
            output: Raw text output from LLM
            messages: Original messages for attribution

        Returns:
            Structured summary result
        """


class BaseModeStrategy(ABC):
    """Base class for mode strategies.

    Provides common functionality and defaults.
    """

    mode_name: str
    mode_version: str = "1"

    @abstractmethod
    def prompt(self, messages: List[Message]) -> str:
        """Generate a prompt from a list of messages."""
        ...

    @abstractmethod
    def parse(self, output: str, messages: List[Message]) -> SummaryResult:
        """Parse LLM output into structured summary."""
        ...


@runtime_checkable
class LLMClient(Protocol):
    """Protocol for LLM provider clients.

    A client is responsible for:
    1. Sending prompts to the LLM provider
    2. Returning raw text outputs
    3. Handling errors (rate limits, timeouts)
    """

    @abstractmethod
    def complete(
        self,
        prompt: str,
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any
    ) -> str:
        """Send a prompt to the LLM and return the completion.

        Args:
            prompt: The prompt text
            model: Model identifier
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional provider-specific parameters

        Returns:
            Raw text output from LLM

        Raises:
            RateLimitError: If rate limited
            TimeoutError: If request times out
            LLMError: For other LLM-related errors
        """


class BaseLLMClient(ABC):
    """Base class for LLM clients.

    Provides common functionality and error handling.
    """

    @abstractmethod
    def complete(
        self,
        prompt: str,
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any
    ) -> str:
        """Send a prompt to the LLM and return the completion."""
        ...


@runtime_checkable
class Store(Protocol):
    """Protocol for storage backends.

    A store is responsible for:
    1. Loading context (prior summaries)
    2. Saving results (new summaries)
    3. Appending to audit logs
    4. Namespace isolation
    """

    @abstractmethod
    def load_context(
        self, namespace: str, memory_level: str = "session"
    ) -> Optional[SummaryResult]:
        """Load prior summary for hierarchical memory.

        Args:
            namespace: Namespace identifier
            memory_level: Memory level (rolling/session/canonical)

        Returns:
            Prior summary or None if not found
        """

    @abstractmethod
    def save_result(
        self,
        namespace: str,
        result: SummaryResult,
        memory_level: str = "session",
    ) -> None:
        """Save a summary result.

        Args:
            namespace: Namespace identifier
            result: Summary to save
            memory_level: Memory level (rolling/session/canonical)
        """

    @abstractmethod
    def append_log(
        self,
        namespace: str,
        operation: str,
        metadata: Dict[str, Any],
    ) -> None:
        """Append to audit log.

        Args:
            namespace: Namespace identifier
            operation: Operation name (e.g., "summarize", "load_context")
            metadata: Operation metadata
        """


class BaseStore(ABC):
    """Base class for store implementations.

    Provides common functionality and validation.
    """

    @abstractmethod
    def load_context(
        self, namespace: str, memory_level: str = "session"
    ) -> Optional[SummaryResult]:
        """Load prior summary for hierarchical memory."""
        ...

    @abstractmethod
    def save_result(
        self,
        namespace: str,
        result: SummaryResult,
        memory_level: str = "session",
    ) -> None:
        """Save a summary result."""
        ...

    @abstractmethod
    def append_log(
        self,
        namespace: str,
        operation: str,
        metadata: Dict[str, Any],
    ) -> None:
        """Append to audit log."""
        ...

