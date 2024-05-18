from ..db import Note
from ..model import NoteRes, NoteReq
from sqlalchemy.orm import scoped_session
from typing import List, Optional


class NoteRepository:
    def __init__(self, db_session: scoped_session):
        self.db_session = db_session

    def get_note_by_id(self, note_id: str) -> NoteRes:
        dbNote: Note = self.db_session.query(Note).filter(Note.id == note_id).first()
        return NoteRes(
            id=dbNote.id,
            title=dbNote.title,
            content=dbNote.content,
            summary=dbNote.summary,
            subCategories=dbNote.sub_categories,
            comments=dbNote.comments,
        )

    def create_note(self, note: NoteReq):
        dbNote = Note(
            title=note.title,
            summary=note.summary,
            image_id=note.image_id,
            categories=note.categories,
            sub_categories=note.sub_categories,
        ).returning(Note.id)

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
