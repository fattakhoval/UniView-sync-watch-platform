import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


class Config:

    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL")

        self.BASE_DIR = Path().absolute()

        self.VOICE_DIR = self.BASE_DIR / Path('src') / Path("media/voices")
        self.VOICE_DIR.mkdir(parents=True, exist_ok=True)

        self.VIDEO_DIR = self.BASE_DIR / Path('src') / Path('media/video')
        self.VIDEO_DIR.mkdir(parents=True, exist_ok=True)


config = Config()
