from typing import Optional

from pydantic import BaseModel
from datetime import date


class Note(BaseModel):
    id: int
    title: str
    text: str
    owner: str
    created_at: date

    class Config:
        from_attributes = True

class NoteCreate(BaseModel):
    title: str
    text: str
    owner: str
    created_at: Optional[date] = None

    class Config:
        from_attributes = True