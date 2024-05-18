from ..db import Category, SubCategory, CategorySubCategory
from ..model import NotesCategoriesGetResponse, NotesCategoriesCategoryIdGetResponse
from sqlalchemy.orm import scoped_session
from sqlalchemy.sql import text
from typing import List
import uuid


class CategoryRepository:
    def __init__(self, db_session: scoped_session):
        self.db_session = db_session

    def get_categories(self) -> NotesCategoriesGetResponse:
        dbCategories: List[Category] = self.db_session.query(Category).distinct().all()
        return NotesCategoriesGetResponse(
            categories=[category for category in dbCategories]
        )

    def get_sub_categories(
        self, category_id: str
    ) -> NotesCategoriesCategoryIdGetResponse:
        dbSubCategories: List[SubCategory] = (
            self.db_session.query(SubCategory)
            .join(CategorySubCategory)
            .filter(CategorySubCategory.category_id == category_id)
            .all()
        )
        return NotesCategoriesCategoryIdGetResponse(
            categories=[sub_category for sub_category in dbSubCategories]
        )

    def create_category(self, category: str):
        result = self.db_session.execute(
            text("SELECT id FROM categories WHERE name = :name"), {"name": category}
        ).fetchone()

        if result:
            return result[0]

        print("its not exist")
        dbCategory = Category(id=uuid.uuid4(), name=category)

        self.db_session.execute(
            text(
                """
            INSERT INTO categories (id, name)
            VALUES (:id, :name)
            RETURNING id;
            """
            ),
            {"id": dbCategory.id, "name": dbCategory.name},
        )

        return dbCategory.id

    def create_sub_category(self, sub_category: str, category_id: uuid.UUID):
        result = self.db_session.execute(
            text("SELECT id FROM sub_categories WHERE name = :name"),
            {"name": sub_category},
        ).fetchone()
        sub_category_id = None

        if result:
            sub_category_id = result[0]
        else:
            dbSubCategory = SubCategory(id=uuid.uuid4(), name=sub_category)

            self.db_session.execute(
                text(
                    """
                INSERT INTO sub_categories (id, name)
                VALUES (:id, :name)
                RETURNING id;
                """
                ),
                {"id": dbSubCategory.id, "name": dbSubCategory.name},
            )
            sub_category_id = dbSubCategory.id

        self.db_session.execute(
            text(
                """
            INSERT INTO category_sub_categories (category_id, sub_category_id)
            VALUES (:category_id, :sub_category_id);
            """
            ),
            {"category_id": category_id, "sub_category_id": sub_category_id},
        )

        return sub_category_id
