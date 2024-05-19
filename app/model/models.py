# generated by fastapi-codegen:
#   filename:  YNotes.openapi.yaml
#   timestamp: 2024-05-14T01:04:48+00:00

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class NotesCategoriesCategoryIdGetResponse(BaseModel):
    categories: List[str]


class NotesCategoriesGetResponse(BaseModel):
    categories: List[str]


class NoteRes(BaseModel):
    title: str
    categories: List[str]
    summary: Optional[str] = None
    subCategories: List[str]
    tags: List[str]
    url: str = None


class NoteReq(BaseModel):
    title: str
    url: str
    categories: List[str]
    summary: Optional[str] = None
    subCategories: List[str]
    tags: List[str]


class NotesGetResponse(BaseModel):
    notes: List[NoteRes]


class NotesPostRequest(BaseModel):
    file: bytes = Field(..., description="解析対象のノートの画像")


class NotesPostResponse(BaseModel):
    noteId: str
    tags: List[str]
    notes: List[NoteRes]
    url: str = None


class NotesTagsPostRequest(BaseModel):
    tags: List[str] = Field(..., description="追加するタグ")


class NotesTagsPostResponse(BaseModel):
    pass


class NotesTagsPatchRequest(BaseModel):
    tags: List[str] = Field(..., description="新たなタグ")


class NotesTagsPatchResponse(BaseModel):
    pass

class NotesByTagRequest(BaseModel):
    tag: str

class NotesByTagResponse(BaseModel):
    notes: List[NoteRes]