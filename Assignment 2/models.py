from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    """Internal data carrier. Frozen: instances cannot be modified after creation."""
    task_id: int
    title: str
    priority: str
    description: str
    status: str = "pending"
