FROM python:3
ENV PYTHONUNBUFFERED 1
ENV DATABASE_HOST db
ENV REDIS_HOST redis
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/