FROM python:3.12

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app_backend

RUN apt-get update && apt-get install -y libpq-dev

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
