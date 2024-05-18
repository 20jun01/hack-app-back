from ..db import Tag, NoteTag
from ..model import NotesTagsPostRequest, NotesTagsPostResponse
from sqlalchemy.orm import scoped_session


class TagRepository:
    def __init__(self, db_session: scoped_session):
        self.db_session = db_session

    def create_tag(
        self, body: NotesTagsPostRequest, note_id: str
    ) -> NotesTagsPostResponse:
        for tag in body.tags:
            dbTag = Tag(name=tag).returning(Tag.id)
            self.db_session.add(dbTag)
            self.db_session.add(NoteTag(tag_id=dbTag.id, note_id=note_id))

        return NotesTagsPostResponse()

    def update_tag(
        self, body: NotesTagsPostRequest, note_id: str
    ) -> NotesTagsPostResponse:
        self.db_session.query(NoteTag).filter(NoteTag.note_id == note_id).delete()
        for tag in body.tags:
            dbTag = Tag(name=tag).returning(Tag.id)
            self.db_session.add(dbTag)
            self.db_session.add(NoteTag(tag_id=dbTag.id, note_id=note_id))

        return NotesTagsPostResponse()
