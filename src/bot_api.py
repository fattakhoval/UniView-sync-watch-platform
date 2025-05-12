import asyncio
import uuid

import aiohttp

from config import config


class UniViewBot:

    def __init__(self):

        self.uuid = config.BOT_UUID
        self.name = 'UniViewBOT'
        self.token = 'eyJjdHkiOiJqd3QiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiUlNBLU9BRVAtMjU2In0.adwoPRwPaz60TaW4yKuVgp9bdA4plmw9NoAI6luGaCRLi-qtJA_5atTH9hCi0ZaC0lQ36TjzdyNIYZPqc3CI39Qmzz-sc_VdTJ9CYaXjEQpNmFLYLeRV9DMtS11DS2L1FvT3omtTOKBpe5z2A-B37or5kkSRq_2AEUFt_5_JRjdAaH8JXEhgH2E-EXPXOiErXnTLYnp24XEugXHnkBtm2IXGBC_4wNJoeG9wpkZbkdodfhSbhPlyLvh2thxNvs3-r7fAq_qBh8_UgG_xGQ0z0WOJyzjJX9sG_It7mz3TMe48Djp84y2YUD0kC05vi81nQivXkPPHdkFLcwcDSfqhvA.7VF6zWSD7-99xDvROwOP3A.RV6oRYfBFMMaAchCNb-lYEpfrmZ5l-BtQKqQZTLlf7jqmmWKg5FRjzBPnyjvmn7WxUliflK6nxoNa_M-Jg72tGcVIkg6HlA3Om02v1xxHMhp9WJ5k9N4axqeYHML68l2-1pFQe8ORfJGnMzM4ZKJS-kG5d1MPQR7I26TKUxx4ssCspi6b6tfjJ7XXptm75yqkwAalVf0xh4Kq_SidcrmEzmbPYZDi5txsqMKuNuP3xKmhgMI8jRXktVIzvCR2M0qEARAvryda1miSfE2_d8b0znlRB7y-UtxIKqrkomJQTQVT0Z0zBHXBqT7YBiw-e-GOIvemSEY6x8KgXXsVLZtbyUahlJGkKBhFyVOJyBPOU27b4MvQFq8VNXZbHNBDdV3o719SujDxWwJVVtsugmRWb2kW1U13yegG99tvgaufd5C-5-bFHt_ggWbHZPi8VYSxdrN17iRKgAs1BFxfqShFIIlAAqvTXPJ4gHiqfDKmHXi7JBGaGuiH9h2VJ6EZtIWu_hlt4_7iaP8HwFM9mGH4_nQpUliL_6Mcbm1flU8_OM2vOZDHmfd-a0ThaTXUZaxWXtpRm42nTjTs2fPproYkRAMEuytWhOcOiuC_FI6YQFoSf_UBR3EBUxzMorgSEVp2Kt3UIeGkjeqHPVoDBYleGhI6BsoN9zJVJiu-EeV6u7BhBmdRueVElJkYr5Vr8clqZ7XqyDLE6NzRLvFaQJLluuN5kU3Ecx3I3A22LSnuyo.K5QX8QlWTZj9lYeAvHcIqGZlmpLfsFA0BZcjZWpDGbM'
    @property
    def error_message(self):
        return "Вопрос не связан с кино. Я отвечаю только на вопросы о фильмах, актерах или режиссерах."

    @property
    def start_prompt(self):
        return 'Если вопрос не относится фильму или не относится развлекательному медиа(кино\сериал\мультики\музыка) отправь в ответ только False.'

    def prepare_msg(self, message: str, current_video: str | None = None):
        msg = f'Условие: {self.start_prompt}.\n'
        if current_video:
            msg += f'Пользовать смотрит: {current_video}.\n'
        msg += f'Вопрос: {message}'
        return msg

    def is_about_movies(self, question: str) -> bool:
        movie_keywords = [
            "кино", "фильм", "кинематограф", "режиссер", "актер",
            "сценарий", "премьера", "кинотеатр", "франшиза", "сериал", "аниме"
        ]
        return any(keyword in question.lower() for keyword in movie_keywords)

    async def ask(self, question):

        payload = {
            "model": "GigaChat-2",
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }

        async with aiohttp.ClientSession() as session:

            for _ in range(3):

                headers = {
                    'Accept': 'application/json',
                    'Authorization': f'Bearer {self.token}',
                    'Content-Type': 'application/json'
                }

                async with session.post(url=config.SBER_CHAT_URL, headers=headers, json=payload, ssl=False) as response:

                    if response.status == 401:
                        await self.get_access_token()
                        continue

                    if response.status == 200:
                        json_response = await response.json()
                        print(json_response)
                        print(response.status)
                        return json_response.get('choices')[0]['message'].get('content')

                    if response.status == 400:
                        print(await response.json())
                        print(response.status)
            else:
                print('Cannot get send message to ChatAI')
                return None

    async def get_access_token(self):
        url = config.SBER_AUTH_URL
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': str(uuid.uuid4()),
            'Authorization': f'Basic {config.SBER_AUTH_KEY}'
        }
        payload = {
            'scope': ['GIGACHAT_API_PERS']
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, headers=headers, data=payload, ssl=False) as response:
                data = await response.json()
                print(data)
                self.token = data.get('access_token')
                print(self.token)
                print(response.status)

uniview_bot = UniViewBot()

async def mai():
    # await uniview_bot.get_access_token()
    await uniview_bot.ask('Привет! Кто выиграл оскар в 2008году?')


if __name__ == '__main__':
    asyncio.run(mai())