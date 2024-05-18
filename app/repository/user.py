from ..db import User


class UserRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_user_by_id(self, user_id):
        return self.db_session.query(User).filter(User.id == user_id).first()

    def create_user(self, user):
        self.db_session.add(user)
