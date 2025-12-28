from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from notes.models import NoteDB
from notes.schemas import NoteUpdate, NoteCreate, Note
from datetime import date


router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/new",
             response_model=Note,
             status_code=201,
             summary="Создать новую заметку",
             description="Создает новую заметку в базе данных. Если дата создания не указана, используется текущая дата.",
             response_description="Созданная заметка с уникальным ID",
             responses={
                 201: {
                     "description": "Заметка успешно создана",
                     "content": {
                         "application/json": {
                             "example": {
                                 "id": 1,
                                 "title": "Моя заметка",
                                 "text": "Текст заметки",
                                 "owner": "Я",
                                 "created_at": "2025-12-28"
                             }
                         }
                     }
                 },
                 422: {
                     "description": "Ошибка валидации данных"
                 }
             }
             )
def create_note(data: NoteCreate, db: Session = Depends(get_db)):
    note = NoteDB(
        title=data.title,
        text=data.text,
        owner=data.owner,
        created_at = data.created_at or date.today()
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

@router.get("/{id}",
            response_model=Note,
            summary="Получить заметку по ID",
            description="Возвращает одну заметку по уникальному идентификатору",
            response_description="Заметка с указанным ID",
            responses={
                200: {
                    "description": "Заметка найдена",
                    "content": {
                        "application/json": {
                            "example": {
                                "id": 1,
                                "title": "Моя заметка",
                                "text": "Текст заметки",
                                "owner": "Иван",
                                "created_at": "2025-12-28"
                            }
                        }
                    }
                },
                404: {
                    "description": "Заметка не найдена",
                    "content": {
                        "application/json": {
                            "example": {"detail": "Заметка не найдена"}
                        }
                    }
                }
            })
def get_note(id: int, db: Session = Depends(get_db)):
    note = db.query(NoteDB).where(NoteDB.id == id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Заметка не найдена")
    return note

@router.get("/",
            response_model=List[Note],
            summary="Получить список заметок",
            description="Возвращает список заметок с возможностью фильтрации и поиска",
            response_description="Список заметок, соответствующих критериям поиска",
            responses={
                200: {
                    "description": "Список заметок успешно получен",
                    "content": {
                        "application/json": {
                            "example": [
                                {
                                    "id": 1,
                                    "title": "Заметка 1",
                                    "text": "Текст заметки 1",
                                    "owner": "Я",
                                    "created_at": "2025-12-28"
                                },
                                {
                                    "id": 2,
                                    "title": "Заметка 2",
                                    "text": "Текст заметки 2",
                                    "owner": "Не я",
                                    "created_at": "2025-12-27"
                                }
                            ]
                        }
                    }
                }
            })
def get_all_notes(
        db: Session = Depends(get_db),
        owner: Optional[str] = None,
        search: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None):

    query = db.query(NoteDB)

    filters = [
        NoteDB.owner == owner if owner else None,
        ((NoteDB.title.ilike(f"%{search}%")) | (NoteDB.text.ilike(f"%{search}%"))) if search else None,
        NoteDB.created_at >= date_from if date_from else None,
        NoteDB.created_at <= date_to if date_to else None,
    ]

    for f in filters:
        if f is not None:
            query = query.filter(f)

    return query.all()

@router.post("/update/{id}",
             response_model=Note,
             summary="Обновить заметку",
             description="Обновляет существующую заметку. Можно обновить одно или несколько полей.",
             response_description="Обновленная заметка",
             responses={
                 200: {
                     "description": "Заметка успешно обновлена",
                     "content": {
                         "application/json": {
                             "example": {
                                 "id": 1,
                                 "title": "Обновленный заголовок",
                                 "text": "Обновленный текст",
                                 "owner": "Точно не я",
                                 "created_at": "2025-12-28"
                             }
                         }
                     }
                 },
                 404: {
                     "description": "Заметка не найдена",
                     "content": {
                         "application/json": {
                             "example": {"detail": "Заметка не найдена"}
                         }
                     }
                 },
                 422: {
                     "description": "Ошибка валидации данных"
                 }
             })
def update_note(id: int, data: NoteUpdate, db: Session = Depends(get_db)):
    note = db.query(NoteDB).where(NoteDB.id == id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Заметка не найдена")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(note, field, value)

    db.commit()
    db.refresh(note)
    return note

@router.post("/delete/{id}",
             status_code=204,
             summary="Удалить заметку",
             description="Удаляет заметку из базы данных по ID",
             response_description="Заметка успешно удалена (нет содержимого)",
             responses={
                 204: {
                     "description": "Заметка успешно удалена"
                 },
                 404: {
                     "description": "Заметка не найдена",
                     "content": {
                         "application/json": {
                             "example": {"detail": "Заметка не найдена"}
                         }
                     }
                 }
             }
             )
def delete_note(id: int, db: Session = Depends(get_db)):
    note = db.query(NoteDB).where(NoteDB.id == id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Заметка не найдена")

    db.delete(note)
    db.commit()
    return True
