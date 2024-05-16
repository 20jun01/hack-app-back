from sqlalchemy import Column, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime
import uuid

Base = declarative_base()

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, "JST")


def get_now():
    return datetime.datetime.now(JST)


class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=get_now)
    notes = relationship("Note", back_populates="user")


class NoteTag(Base):
    __tablename__ = "note_tags"
    note_id = Column(UUID(as_uuid=True), ForeignKey("notes.note_id"), primary_key=True)
    tag_id = Column(UUID(as_uuid=True), ForeignKey("tags.tag_id"), primary_key=True)


class NoteCategory(Base):
    __tablename__ = "note_categories"
    note_id = Column(UUID(as_uuid=True), ForeignKey("notes.note_id"), primary_key=True)
    category_id = Column(
        UUID(as_uuid=True), ForeignKey("categories.category_id"), primary_key=True
    )


class CategorySubCategory(Base):
    __tablename__ = "category_sub_categories"
    category_id = Column(
        UUID(as_uuid=True), ForeignKey("categories.category_id"), primary_key=True
    )
    sub_category_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sub_categories.sub_category_id"),
        primary_key=True,
    )


class NoteSubCategory(Base):
    __tablename__ = "notes_sub_categories"
    note_id = Column(UUID(as_uuid=True), ForeignKey("notes.note_id"), primary_key=True)
    sub_category_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sub_categories.sub_category_id"),
        primary_key=True,
    )


class Note(Base):
    __tablename__ = "notes"
    note_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    title = Column(String(200), nullable=False)
    image_id = Column(Text)
    summary = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), default=get_now)
    user = relationship("User", back_populates="notes")
    tags = relationship("Tag", secondary=NoteTag.__tablename__, back_populates="notes")
    categories = relationship(
        "Category", secondary=NoteCategory.__tablename__, back_populates="notes"
    )
    sub_categories = relationship(
        "SubCategory", secondary=NoteSubCategory.__tablename__, back_populates="notes"
    )


class Tag(Base):
    __tablename__ = "tags"
    tag_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False)
    notes = relationship("Note", secondary=NoteTag.__tablename__, back_populates="tags")


class Comment(Base):
    __tablename__ = "comments"
    comment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    note_id = Column(UUID(as_uuid=True), ForeignKey("notes.note_id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=get_now)


class Category(Base):
    __tablename__ = "categories"
    category_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False)
    notes = relationship(
        "Note", secondary=NoteCategory.__tablename__, back_populates="categories"
    )
    sub_categories = relationship(
        "SubCategory",
        secondary=CategorySubCategory.__tablename__,
        back_populates="categories",
    )


class SubCategory(Base):
    __tablename__ = "sub_categories"
    sub_category_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False)
    categories = relationship(
        "Category",
        secondary=CategorySubCategory.__tablename__,
        back_populates="sub_categories",
    )
    notes = relationship(
        "Note", secondary=NoteSubCategory.__tablename__, back_populates="sub_categories"
    )
