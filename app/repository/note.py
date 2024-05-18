from ..db import Note, Category, SubCategory, Tag, NoteCategory, NoteSubCategory, NoteTag
from ..model import NoteRes, NoteReq
from sqlalchemy.orm import scoped_session
from typing import List, Optional
import uuid


class NoteRepository:
    def __init__(self, db_session: scoped_session):
        self.db_session = db_session

    def create_note_tag(self, note_id: str, tag_ids: List[str]):
        note_tags = [
            NoteTag(
                note_id=note_id,
                tag_id=tag_id,
            ) for tag_id in tag_ids
        ]
        self.db_session.add_all(note_tags)


    def create_note_category(self, note_id: str, category_ids: List[str]):
        note_categories = [
            NoteCategory(
                note_id=note_id,
                category_id=category_id,
            ) for category_id in category_ids
        ]
        self.db_session.add_all(note_categories)

    def create_note_sub_category(self, note_id: str, sub_category_ids: List[str]):
        note_sub_categories = [
            NoteSubCategory(
                note_id=note_id,
                sub_category_id=sub_category_id,
            ) for sub_category_id in sub_category_ids
        ]
        self.db_session.add_all(note_sub_categories)

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

    def create_note(self, note: NoteReq, category_ids: List[str], sub_category_ids_map: dict, tag_ids: List[str]):
        dbNote: Note = Note(
            user_id=uuid.uuid4(),
            title=note.title,
            image_id=note.url,
            summary=note.summary,
        )
        self.db_session.add(dbNote)

        self.create_note_category(dbNote.id, category_ids)
        self.create_note_sub_category(dbNote.id, sub_category_ids_map)
        self.create_note_tag(dbNote.id, tag_ids)

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
