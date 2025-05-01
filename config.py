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

        self.DEEPSEEK_API_URL = os.getenv('DEEPSEEK_API_URL')
        self.DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

        self.SBER_AUTH_URL = os.getenv('SBER_AUTH_URL')
        self.SBER_CHAT_URL = os.getenv('SBER_CHAT_URL')
        self.SBER_CLIENT_ID = os.getenv('SBER_CLIENT_ID')
        self.SBER_AUTH_KEY = os.getenv('SBER_AUTH_KEY')

        self.BOT_UUID = os.getenv('BOT_UUID')


config = Config()
