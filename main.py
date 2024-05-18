# generated by fastapi-codegen:
#   filename:  YNotes.openapi.yaml
#   timestamp: 2024-05-14T01:04:48+00:00

from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, Path, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from io import BufferedReader
from sqlalchemy.orm import Session
from typing import Generator

from app import (
    NotesCategoriesCategoryIdGetResponse,
    NotesCategoriesGetResponse,
    NotesGetResponse,
    NotesPostResponse,
    NoteReq,
    NotesTagsPatchRequest,
    NotesTagsPatchResponse,
    NotesTagsPostRequest,
    NotesTagsPostResponse,
    Database,
    Config,
    MyS3Client,
    ChatGPTAPI,
    CategoryRepository,
    TagRepository,
    NoteRepository,
    ChatGPTResponse,
    encode_image_base64,
)


class Main:
    def __init__(self):
        config = Config()
        self.db = Database(
            config.DB_HOST, config.DB_NAME, config.DB_USER, config.DB_PASSWORD
        )

        self.s3 = MyS3Client(config.S3_BUCKET_NAME)
        self.chatgpt = ChatGPTAPI(config.OPEN_AI_API_KEY, config.OPEN_AI_ORGANIZATION_ID)

        self.app = FastAPI(
            title="YNotes",
            description="",
            version="1.0.0",
        )

        origins = [
            "http://localhost:8080",
            "http://localhost:8080/",
        ]

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            self.db.migrate()
            yield

        self.app.router.lifespan_context = lifespan

        @self.app.get("/notes", response_model=NotesGetResponse)
        def get_notes(
            keyword: Optional[str] = None,
            db_session: Generator[Session, None, None] = Depends(
                self.db.get_db_session
            ),
        ) -> NotesGetResponse:
            """
            検索
            """
            with db_session as db_session:
                note_repo = NoteRepository(db_session)
                notes = note_repo.get_notes(keyword)

                return NotesGetResponse(notes=notes)

        @self.app.post("/notes", response_model=NotesPostResponse)
        async def post_notes(
            file: UploadFile,
            db_session: Generator[Session, None, None] = Depends(
                self.db.get_db_session
            ),
        ) -> NotesPostResponse:
            """
            解析
            """
            with db_session as db_session:
                # initialize repository
                note_repo = NoteRepository(db_session)

                file_object: BufferedReader = file.file
                file_bytes: bytes = file_object.read()

                image_base64 = encode_image_base64(file_bytes)
                response: ChatGPTResponse = self.chatgpt.describe_image(image_base64)
                file_extension: str = file.filename.split(".")[-1]
                image_url = self.s3.upload_image(file_object, file_extension)
                note_req =  NoteReq(
                    title=response.title,
                    url=image_url,
                    categories=[response.category],
                    summary=response.summary,
                    subCategories=[response.subcategory],
                    tags=response.tags,
                )
                note_id = note_repo.create_note(note_req)
                return NotesPostResponse(noteId=note_id, tags=response.tags)

        @self.app.get("/notes/categories", response_model=NotesCategoriesGetResponse)
        def get_notes_categories(
            db_session: Generator[Session, None, None] = Depends(
                self.db.get_db_session
            ),
        ) -> NotesCategoriesGetResponse:
            """
            分類取得
            """
            with db_session as db_session:
                category_repo = CategoryRepository(db_session)
                categories = category_repo.get_categories()
                return NotesCategoriesGetResponse(categories=categories)

        @self.app.get(
            "/notes/categories/{categoryId}",
            response_model=NotesCategoriesCategoryIdGetResponse,
        )
        def get_notes_categories_category_id(
            category_id: str = Path(..., alias="categoryId"),
            db_session: Generator[Session, None, None] = Depends(
                self.db.get_db_session
            ),
        ) -> NotesCategoriesCategoryIdGetResponse:
            """
            副分類取得
            """
            with db_session as db_session:
                category_repo = CategoryRepository(db_session)
                categories = category_repo.get_sub_categories(category_id)
                return NotesCategoriesCategoryIdGetResponse(categories=categories)

        @self.app.post(
            "/notes/{noteId}/tags",
            response_model=NotesTagsPostResponse,
        )
        def post_notes_tags(
            body: NotesTagsPostRequest = None,
            note_id: str = Path(..., alias="noteId"),
            db_session: Generator[Session, None, None] = Depends(
                self.db.get_db_session
            ),
        ) -> NotesTagsPostResponse:
            """
            タグ作成
            """
            with db_session as db_session:
                tag_repo = TagRepository(db_session)
                response = tag_repo.create_tag(body, note_id)
                return response

        @self.app.patch(
            "/notes/{noteId}/tags",
            response_model=NotesTagsPatchResponse,
        )
        def patch_notes_tags(
            body: NotesTagsPatchRequest = None,
            note_id: str = Path(..., alias="noteId"),
            db_session: Generator[Session, None, None] = Depends(
                self.db.get_db_session
            ),
        ) -> NotesTagsPatchResponse:
            """
            タグ更新
            """
            with db_session as db_session:
                tag_repo = TagRepository(db_session)
                response = tag_repo.update_tag(body, note_id)
                return response


if __name__ == "__main__":
    import uvicorn

    main = Main()
    uvicorn.run(main.app, host="0.0.0.0", port=8000)
