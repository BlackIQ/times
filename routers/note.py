# FastAPI
from fastapi import APIRouter, Depends, HTTPException, status

# SQLAlchemy
from sqlalchemy.orm import Session

# Datetime
from datetime import datetime, timezone

# Application
from dependencies.db import get_db  # Get Database
from dependencies.auth import get_current_user  # Get Current User
from schemas.note import NoteCreate, NoteUpdate, NoteRead  # Schemas
from models import Note, User  # Models

# Router
router = APIRouter(
    prefix="/notes",
    tags=["Note"],
)


@router.get("/user/{user_id}", response_model=list[NoteRead])
async def list_user_notes(
    user_id: int,
    db: Session = Depends(get_db),
):
    notes = (
        db.query(Note)
        .where(
            Note.user_id == user_id,
            Note.deleted_at.is_(None),
        )
        .all()
    )

    return notes


@router.get("/trash", response_model=list[NoteRead])
async def list_user_deleted_notes(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    notes = (
        db.query(Note)
        .where(
            Note.user_id == user.id,
            Note.deleted_at.is_not(None),
        )
        .all()
    )

    return notes


@router.get("/{note_id}", response_model=NoteRead)
async def get_note(
    note_id: int,
    db: Session = Depends(get_db),
):
    note = (
        db.query(Note)
        .where(
            Note.id == note_id,
            Note.deleted_at.is_(None),
        )
        .one_or_none()
    )

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found",
        )

    return note


@router.post("", response_model=NoteRead)
async def create_note(
    note: NoteCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    slug_exists = db.query(Note).where(Note.slug == note.slug).first()
    if slug_exists:
        raise HTTPException(
            status_code=409,
            detail="Slug already exists",
        )

    db_note = Note(**note.model_dump(), user_id=user.id)

    db.add(db_note)

    db.commit()
    db.refresh(db_note)

    return db_note


@router.patch("/{note_id}", response_model=NoteRead)
async def update_note(
    note_id: int,
    note_data: NoteUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    note = (
        db.query(Note)
        .where(
            Note.id == note_id,
            Note.deleted_at.is_(None),
        )
        .one_or_none()
    )

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found",
        )

    if note.user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You can not change another one notes",
        )

    slug_exists = (
        db.query(Note)
        .where(
            Note.slug == note_data.slug,
            Note.id != note.id,
        )
        .first()
    )
    if slug_exists:
        raise HTTPException(
            status_code=409,
            detail="Slug already exists",
        )

    data = note_data.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(note, key, value)

    db.commit()
    db.refresh(note)

    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_note(
    note_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    note = (
        db.query(Note)
        .where(
            Note.id == note_id,
            Note.deleted_at.is_(None),
        )
        .one_or_none()
    )

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found",
        )

    if note.user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You can not change another one notes",
        )

    note.deleted_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(note)

    return None


@router.post("/{note_id}/restore", status_code=status.HTTP_204_NO_CONTENT)
async def restore_note(
    note_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    note = (
        db.query(Note)
        .where(
            Note.id == note_id,
            Note.deleted_at.is_note(None),
        )
        .one_or_none()
    )

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found",
        )

    if note.user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You can not change another one notes",
        )

    note.deleted_at = None

    db.commit()
    db.refresh(note)

    return None


@router.delete("/{note_id}/force", status_code=status.HTTP_204_NO_CONTENT)
async def hard_delete_note(
    note_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    note = (
        db.query(Note)
        .where(
            Note.id == note_id,
            Note.deleted_at.is_not(None),
        )
        .one_or_none()
    )

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found",
        )

    if note.user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You can not change another one notes",
        )

    db.delete(note)

    db.commit()

    return None
