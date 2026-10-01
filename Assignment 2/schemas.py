from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator

Priority = Literal["low", "medium", "high"]


def _check_uppercase_start(value: str) -> str:
    if not value[0].isupper():
        raise ValueError("title must start with an uppercase letter")
    return value


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    priority: Priority
    description: Optional[str] = "No description"

    @field_validator("title")
    @classmethod
    def title_must_be_capitalized(cls, v: str) -> str:
        return _check_uppercase_start(v)


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=50)
    priority: Optional[Priority] = None
    description: Optional[str] = None

    @field_validator("title")
    @classmethod
    def title_must_be_capitalized(cls, v: Optional[str]) -> Optional[str]:
        # Rule applies only when a title is provided (important for PATCH)
        if v is None:
            return v
        return _check_uppercase_start(v)


class TaskResponse(BaseModel):
    task_id: int
    title: str
    priority: str
    description: str
    status: str


if __name__ == "__main__":
    # Serialization demo: model -> dict and model -> JSON
    task = TaskCreate(title="Write report", priority="high")
    print("dict:", task.model_dump())
    print("json:", task.model_dump_json())
