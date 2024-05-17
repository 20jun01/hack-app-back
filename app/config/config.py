import os
from dotenv import load_dotenv
import json
from logging import getLogger, config


class Config:
    def __init__(self) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "data/log_config.json")
        with open(file_path) as f:
            log_conf = json.load(f)

            config.dictConfig(log_conf)

        load_dotenv()
        self.DB_HOST = os.getenv("DB_HOST", "localhost")
        self.DB_NAME = os.getenv("DB_NAME", "postgres")
        self.DB_PORT = os.getenv("DB_PORT", "5432")
        self.DB_USER = os.getenv("DB_USER", "root")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
        self.OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY", "")
