import os
from dotenv import load_dotenv

class Config:
    def __init__(self) -> None:
        load_dotenv()
        self.DB_HOST = os.getenv('DB_HOST', 'localhost')
        self.DB_NAME = os.getenv('DB_NAME', 'postgres')
        self.DB_PORT = os.getenv('DB_PORT', '5432')
        self.DB_USER = os.getenv('DB_USER', 'root')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
        self.OPEN_AI_API_KEY = os.getenv('OPEN_AI_API_KEY', '')