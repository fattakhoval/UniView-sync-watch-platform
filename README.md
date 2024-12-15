
Для запуска celery  `celery -A core.celery worker --loglevel=info`


для запуска проект `uvicorn core.asgi:application --host 127.0.0.1 --port 8000 --reload
`