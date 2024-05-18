from ..db import Tag, NoteTag
from ..model import NotesTagsPostRequest, NotesTagsPostResponse
from sqlalchemy.orm import scoped_session
from sqlalchemy.sql import text
from typing import List
import uuid


class TagRepository:
    def __init__(self, db_session: scoped_session):
        self.db_session = db_session

    def create_tag(self, body: NotesTagsPostRequest) -> NotesTagsPostResponse:
        tag_ids = []
        for tag in set(body.tags):
            result = self.db_session.execute(
                text("SELECT id FROM tags WHERE name = :name"), {"name": tag}
            ).fetchone()

            if result:
                tag_id = result[0]
                tag_ids.append(tag_id)
                continue
            dbTag = self.db_session.execute(
                text(
                    """
                INSERT INTO tags (name)
                VALUES (:name)
                ON CONFLICT (name) DO UPDATE
                SET name = EXCLUDED.name
                RETURNING id;
                """
                ),
                {"name": tag},
            )

    def create_tags(self, tags: List[str]) -> List[uuid.UUID]:
        tag_ids = []
        for tag in tags:
            result = self.db_session.execute(
                text("SELECT id FROM tags WHERE name = :name"), {"name": tag}
            ).fetchone()

            if result:
                tag_id = result[0]
                tag_ids.append(tag_id)
                continue
            dbTag = Tag(id=uuid.uuid4(), name=tag)
            self.db_session.add(dbTag)
            tag_ids.append(dbTag.id)

        return tag_ids

    def update_tag(
        self, body: NotesTagsPostRequest, note_id: str
    ) -> NotesTagsPostResponse:
        self.db_session.query(NoteTag).filter(NoteTag.note_id == note_id).delete()
        for tag in body.tags:
            dbTag = Tag(name=tag).returning(Tag.id)
            self.db_session.add(dbTag)
            self.db_session.add(NoteTag(tag_id=dbTag.id, note_id=note_id))

        return NotesTagsPostResponse()
