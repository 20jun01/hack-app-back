from ..db import Category, SubCategory, CategorySubCategory
from ..model import NotesCategoriesGetResponse, NotesCategoriesCategoryIdGetResponse
from sqlalchemy.orm import scoped_session
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
        dbCategory = Category(id=uuid.uuid4(), name=category)
        self.db_session.add(dbCategory)
        return dbCategory.id

    def create_sub_category(self, sub_category: str, category_id: uuid.UUID):
        dbSubCategory = SubCategory(id=uuid.uuid4(), name=sub_category)

        self.db_session.add(dbSubCategory)
        self.db_session.flush()
        self.db_session.add(
            CategorySubCategory(
                category_id=category_id, sub_category_id=dbSubCategory.id
            )
        )
        return dbSubCategory.id
