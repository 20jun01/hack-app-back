from ..db import Category, SubCategory, CategorySubCategory
from ..model import NotesCategoriesGetResponse, NotesCategoriesCategoryIdGetResponse
from sqlalchemy.orm import scoped_session
from typing import List


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
