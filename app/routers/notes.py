from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from notes.models import NoteDB
from notes.schemas import NoteCreate, Note
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