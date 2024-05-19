from ..db import Note, NoteCategory, NoteSubCategory, NoteTag, Tag
from ..model import NoteRes, NoteReq
from sqlalchemy.orm import scoped_session
from typing import List, Optional
import uuid
from sqlalchemy.orm.exc import NoResultFound

class NoteRepository:
    def __init__(self, db_session: scoped_session):
        self.db_session = db_session

    def create_note_tag(self, note_id: str, tag_ids: List[str]):
        note_tags = [
            NoteTag(
                note_id=note_id,
                tag_id=tag_id,
            )
            for tag_id in tag_ids
        ]
        self.db_session.add_all(note_tags)

    def update_note_tag(self, note_id: str, tag_ids: List[str]):
        self.db_session.query(NoteTag).filter(NoteTag.note_id == note_id).delete()
        self.create_note_tag(note_id, tag_ids)

    def create_note_category(self, note_id: str, category_ids: List[str]):
        note_categories = [
            NoteCategory(
                note_id=note_id,
                category_id=category_id,
            )
            for category_id in category_ids
        ]
        self.db_session.add_all(note_categories)

    def create_note_sub_category(self, note_id: str, sub_category_ids: List[str]):
        note_sub_categories = [
            NoteSubCategory(
                note_id=note_id,
                sub_category_id=sub_category_id,
            )
            for sub_category_id in sub_category_ids
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
            url=dbNote.image_id
        )

    def create_note(
        self,
        note: NoteReq,
        category_ids: List[uuid.UUID],
        sub_category_ids_map: dict,
        tag_ids: List[uuid.UUID],
        user_id: uuid.UUID,
    ):
        dbNote: Note = Note(
            id=uuid.uuid4(),
            user_id=user_id,
            title=note.title,
            image_id=note.url,
            summary=note.summary,
        )
        self.db_session.add(dbNote)
        self.db_session.commit()

        self.create_note_category(dbNote.id, category_ids)
        for v in category_ids:
            self.create_note_sub_category(dbNote.id, sub_category_ids_map[v])
        self.create_note_tag(dbNote.id, tag_ids)

        return dbNote.id

    def get_notes(self, keyword: Optional[str] = None) -> List[NoteRes]:
        print(keyword)
        if keyword:
            dbNotes: List[Note] = (
                self.db_session.query(Note)
                .filter(Note.title.ilike(f"%{keyword}%"))
                .all()
            )
        else:
            dbNotes: List[Note] = self.db_session.query(Note).all()
        print(dbNotes)
        return [
            NoteRes(
                title=dbNote.title,
                categories=[category.name for category in dbNote.categories],
                summary=dbNote.summary,
                subCategories=[
                    sub_category.name for sub_category in dbNote.sub_categories
                ],
                tags=[
                    tag.name for tag in dbNote.tags
                ],
                url=dbNote.image_id
            )
            for dbNote in dbNotes
        ]
    
    def get_notes_by_tag(self, tag: str) -> List[NoteRes]:
        dbNotes: List[Note] = (
            self.db_session.query(Note)
            .join(NoteTag)
            .join(Tag)
            .filter(Tag.name == tag)
            .all()
        )
        return [
            NoteRes(
                title=dbNote.title,
                categories=[category.name for category in dbNote.categories],
                summary=dbNote.summary,
                subCategories=[
                    sub_category.name for sub_category in dbNote.sub_categories
                ],
                tags=[
                    tag.name for tag in dbNote.tags
                ],
                url=dbNote.image_id
            )
            for dbNote in dbNotes
        ]