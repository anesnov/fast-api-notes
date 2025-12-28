from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from notes.models import NoteDB
from notes.schemas import NoteUpdate, NoteCreate, Note
from datetime import date


router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/new", response_model=Note)
def create_source(data: NoteCreate, db: Session = Depends(get_db)):
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

@router.get("/{id}", response_model=Note)
def get_note(id: int, db: Session = Depends(get_db)):
    note = db.query(NoteDB).where(NoteDB.id == id).first()
    return note

@router.get("/", response_model=List[Note],
            description="Получение списка всех заметок")
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
