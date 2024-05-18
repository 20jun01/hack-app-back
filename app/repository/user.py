from ..db import User
from sqlalchemy.orm import scoped_session
import uuid
import hashlib


class UserRepository:
    def __init__(self, db_session: scoped_session):
        self.db_session = db_session

    def get_user_by_id(self, user_id):
        return self.db_session.query(User).filter(User.id == user_id).first()

    def create_user(self, user_name: str, email: str, password: str) -> uuid.UUID:
        user = self.db_session.query(User).filter(User.username == user_name).first()
        if user:
            return user.id
        user = User(
            id=uuid.uuid4(),
            username=user_name,
            email=email,
            password=hashlib.md5(password.encode('utf-8')).hexdigest(),
        )
        self.db_session.add(user)
        self.db_session.commit()
        return user.id
