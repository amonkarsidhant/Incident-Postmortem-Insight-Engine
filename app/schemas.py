from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class EvaluatorActionItem(BaseModel):
    description: str
    owner: str
    due_date: str


class EvaluatorResult(BaseModel):
    summary: str
    severity: str
    action_items: List[EvaluatorActionItem] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)


class PostmortemBase(BaseModel):
    owner: str
    file_path: str
    evaluator_json: Optional[EvaluatorResult] = None

    class Config:
        orm_mode = True


class PostmortemRead(PostmortemBase):
    id: UUID
    created_at: datetime
