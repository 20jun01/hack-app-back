import psycopg2
from .config import Config

class Database:
    def __init__(self, config: Config):
        # データベースとのコネクションを確立します。
        self.connection = psycopg2.connect(f"host={config.DB_HOST} dbname={config.DB_NAME} user={config.DB_USER} password={config.DB_PASSWORD}")

        # カーソルをオープンします。
        cursor = self.connection.cursor()
