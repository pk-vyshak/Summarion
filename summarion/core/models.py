"""
Pydantic models for the summarization framework.

This module contains all data structures used throughout the framework:
- Message: Individual messages from conversations
- SummaryResult: The output of summarization
- Component models: AttributedPoint, Decision, Task, Event
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    """Represents a single message in a conversation.

    Attributes:
        id: Unique message identifier
        role: Role of the speaker (user, assistant, system, etc.)
        content: Message text content
        timestamp: Timestamp when the message was sent (ISO format)
    """

    id: str = Field(description="Unique message identifier")
    role: str = Field(description="Role of the speaker (user, assistant, system)")
    content: str = Field(description="Message text content")
    timestamp: Optional[str] = Field(
        default=None, description="ISO timestamp when message was sent"
    )


class AttributedPoint(BaseModel):
    """A key point with attribution to source messages.

    Attributes:
        text: The extracted point text
        source_msg_ids: Message IDs that contributed to this point
    """

    text: str = Field(description="The extracted point text")
    source_msg_ids: List[str] = Field(
        default_factory=list,
        description="Message IDs that contributed to this point",
    )


class Decision(BaseModel):
    """A decision with context and attribution.

    Attributes:
        decision: The decision text
        rationale: Why this decision was made
        owner: Who owns/responsible for this decision
        date: When the decision was made (ISO date format)
        source_msg_ids: Message IDs that contributed to this decision
    """

    decision: str = Field(description="The decision text")
    rationale: str = Field(description="Why this decision was made")
    owner: Optional[str] = Field(default=None, description="Decision owner/responsible")
    date: Optional[str] = Field(
        default=None, description="ISO date when decision was made"
    )
    source_msg_ids: List[str] = Field(
        default_factory=list,
        description="Message IDs that contributed to this decision",
    )


class Task(BaseModel):
    """A task with assignee and priority.

    Attributes:
        task: The task description
        owner: Who is assigned to this task
        due: Due date (ISO date format)
        priority: Priority level (high, medium, low)
        source_msg_ids: Message IDs that contributed to this task
    """

    task: str = Field(description="The task description")
    owner: Optional[str] = Field(default=None, description="Task owner/assignee")
    due: Optional[str] = Field(default=None, description="Due date (ISO format)")
    priority: Optional[str] = Field(
        default=None, description="Priority level (high/medium/low)"
    )
    source_msg_ids: List[str] = Field(
        default_factory=list,
        description="Message IDs that contributed to this task",
    )


class Event(BaseModel):
    """A chronological event with timestamp.

    Attributes:
        timestamp: When the event occurred (ISO timestamp)
        event: Description of the event
        source_msg_ids: Message IDs that contributed to this event
    """

    timestamp: str = Field(description="ISO timestamp when event occurred")
    event: str = Field(description="Description of the event")
    source_msg_ids: List[str] = Field(
        default_factory=list,
        description="Message IDs that contributed to this event",
    )


class SummaryResult(BaseModel):
    """The output of summarization.

    This is the main data structure that contains all summarization results.
    Different modes populate different fields based on their purpose.

    Attributes:
        mode: The mode used for summarization
        title: Optional title for the summary
        points: List of key points (for pointwise mode)
        decisions: List of key decisions (for key_decisions mode)
        timeline: List of chronological events (for timeline mode)
        tasks: List of action items/tasks
        summary: Freeform narrative summary
        metadata: Additional metadata (cost, tokens, etc.)
        created_at: Timestamp when summary was created
    """

    mode: str = Field(description="The mode used for summarization")
    title: Optional[str] = Field(default=None, description="Optional title")
    points: List[AttributedPoint] = Field(
        default_factory=list, description="Key points"
    )
    decisions: List[Decision] = Field(default_factory=list, description="Key decisions")
    timeline: List[Event] = Field(
        default_factory=list, description="Chronological events"
    )
    tasks: List[Task] = Field(default_factory=list, description="Action items/tasks")
    summary: Optional[str] = Field(default=None, description="Freeform narrative")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )
    created_at: Optional[str] = Field(
        default=None, description="ISO timestamp when summary was created"
    )


class SummarizerConfig(BaseModel):
    """Configuration for the summarizer.

    Attributes:
        namespace: Namespace identifier for multi-tenancy
        llm_provider: LLM provider name (e.g., 'openai', 'anthropic')
        max_tokens: Maximum tokens per request
        max_cost_usd: Maximum cost in USD per operation
        temperature: Sampling temperature
        enable_pii_redaction: Whether to enable PII redaction
        memory_level: Memory level (rolling/session/canonical)
    """

    namespace: str = Field(description="Namespace identifier")
    llm_provider: str = Field(default="openai", description="LLM provider")
    max_tokens: int = Field(default=4000, description="Max tokens per request")
    max_cost_usd: float = Field(default=0.05, description="Max cost in USD")
    temperature: float = Field(default=0.7, description="Sampling temperature")
    enable_pii_redaction: bool = Field(
        default=True, description="Enable PII redaction"
    )
    memory_level: str = Field(default="session", description="Memory level")

