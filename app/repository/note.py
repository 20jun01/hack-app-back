from ..db import Note, Category, SubCategory, Tag
from ..model import NoteRes, NoteReq
from sqlalchemy.orm import scoped_session
from typing import List, Optional
import uuid


class NoteRepository:
    def __init__(self, db_session: scoped_session):
        self.db_session = db_session

    def get_note_by_id(self, note_id: str) -> NoteRes:
        dbNote: Note = self.db_session.query(Note).filter(Note.id == note_id).first()
        return NoteRes(
            id=dbNote.id,
            title=dbNote.title,
            summary=dbNote.summary,
            subCategories=dbNote.sub_categories,
            categories=dbNote.categories,
            tags=dbNote.tags,
        )

    def create_note(self, note: NoteReq):
        categories: List[Category] = [
            Category(
                name=category,
            ) for category in note.categories
        ]
        subcategories: List[SubCategory] = [
            SubCategory(
                name=subcategory,
            ) for subcategory in note.subCategories
        ]
        tags: List[Tag] = [
            Tag(
                name=tag,
            ) for tag in note.tags
        ]

        dbNote: Note = Note(
            user_id=uuid.uuid4(),
            title=note.title,
            image_id=note.url,
            summary=note.summary,
            categories=categories,
            sub_categories=subcategories,
            tags=tags,
        )
        self.db_session.add(dbNote)

        return dbNote.id

    def get_notes(self, keyword: Optional[str] = None) -> List[NoteRes]:
        if keyword:
            dbNotes: List[Note] = (
                self.db_session.query(Note)
                .filter(Note.title.ilike(f"%{keyword}%"))
                .all()
            )
        else:
            dbNotes: List[Note] = self.db_session.query(Note).all()
        return [
            NoteRes(
                id=dbNote.id,
                categories=dbNote.categories,
                title=dbNote.title,
                summary=dbNote.summary,
                subCategories=dbNote.sub_categories,
            )
            for dbNote in dbNotes
        ]
