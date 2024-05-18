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
            categories=[category.name for category in dbCategories]
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
            categories=[sub_category.name for sub_category in dbSubCategories]
        )

    def create_category(self, category: str):
        result = self.db_session.execute(
            text("SELECT id FROM categories WHERE name = :name"), {"name": category}
        ).fetchone()

        if result:
            return result[0]

        dbCategory = Category(id=uuid.uuid4(), name=category)

        self.db_session.add(dbCategory)
        self.db_session.commit()

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

            self.db_session.add(dbSubCategory)
            sub_category_id = dbSubCategory.id
            self.db_session.commit()
        if self.db_session.query(CategorySubCategory).filter(
            CategorySubCategory.category_id == category_id,
            CategorySubCategory.sub_category_id == sub_category_id,
        ).first():
            return sub_category_id
        self.db_session.add(
            CategorySubCategory(
                category_id=category_id, sub_category_id=sub_category_id
            )
        )
        
        self.db_session.commit()
        return sub_category_id
