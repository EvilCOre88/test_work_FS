# Использовать официальный образ родительского образа / слепка.
FROM python:3.10
# set work directory
WORKDIR .
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt .
RUN pip install -r requirements.txt
# copy project
COPY . .
ENTRYPOINT ["sh", "entrypoint.sh"]
CMD celery -A test_work_FS worker -l info -P gevent