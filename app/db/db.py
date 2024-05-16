from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from .models import Base

class Database:
    def __init__(self, DB_HOST: str, DB_NAME: str, DB_USER: str, DB_PASSWORD: str) -> None:
        self.DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
        self.engine = create_engine(self.DATABASE_URL)
        self.SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))

    # with句で使えるメソッドを定義
    @contextmanager
    def get_db_session(self):
        # 前処理
        session = self.SessionLocal()
        try:
            # withで渡す値
            yield session
            # 後処理
            session.commit()
        except Exception:
            # エラーが発生した場合の後処理
            session.rollback()
            raise
        finally:
            # 後処理
            session.close()

    def migrate(self):
        Base.metadata.create_all(self.engine)