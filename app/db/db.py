import psycopg2
from ..model import *

class Database:
    def __init__(self, DB_HOST: str, DB_NAME: str, DB_USER: str, DB_PASSWORD: str) -> None:
        # データベースとのコネクションを確立します。
        self.connection = psycopg2.connect(f"host={DB_HOST} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD}")

        # カーソルをオープンします。
        self.cursor = self.connection.cursor()
