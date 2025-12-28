from typing import Optional

from pydantic import BaseModel, Field
from datetime import date


class Note(BaseModel):
    id: int = Field(
        ...,
        description="Уникальный идентификатор заметки",
        examples=[1, 42]
    )
    title: str = Field(
        ...,
        description="Заголовок заметки",
        examples=["Моя заметка"]
    )
    text: str = Field(
        ...,
        description="Текст заметки",
        examples=["Это текст моей заметки"]
    )
    owner: str = Field(
        ...,
        description="Владелец заметки",
        examples=["Иван"]
    )
    created_at: date = Field(
        ...,
        description="Дата и время создания заметки",
        examples=["2025-12-28"]
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Моя первая заметка",
                "text": "Это пример текста заметки",
                "owner": "Я",
                "created_at": "2025-12-28"
            }
        }


class NoteCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Заголовок заметки",
        examples=["Важная встреча"]
    )
    text: str = Field(
        ...,
        min_length=1,
        description="Текст заметки",
        examples=["Встреча с клиентом в 14:00"]
    )
    owner: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Имя владельца заметки",
        examples=["Иван"]
    )
    created_at: Optional[date] = Field(
        None,
        description="Дата создания заметки. Если не указана, используется текущая дата",
        examples=["2025-12-28"]
    )

class NoteUpdate(BaseModel):
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="Новый заголовок заметки",
        examples=["Обновленный заголовок"]
    )
    text: Optional[str] = Field(
        None,
        min_length=1,
        description="Новый текст заметки",
        examples=["Обновленный текст заметки"]
    )
    owner: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Новый владелец заметки",
        examples=["Иван"]
    )
    created_at: Optional[date] = Field(
        None,
        description="Новая дата создания",
        examples=["2025-12-28"]
    )
