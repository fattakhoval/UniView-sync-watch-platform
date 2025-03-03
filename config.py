import os
from dotenv import load_dotenv


load_dotenv()


class Config:

    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL")



config = Config()
