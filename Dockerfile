# Использовать официальный образ родительского образа / слепка.
FROM python:3.10
# Установка рабочей директории, откуда выполняются команды внутри контейнера.
WORKDIR /usr/src/app
# Добавляем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .
# Добавить мета-информацию к образу для открытия порта к прослушиванию.
EXPOSE 8000
# Выполнить команду внутри контейнера
CMD python manage.py runserver 0.0.0.0:8000
CMD celery -A test_work_FS worker -l info -P gevent