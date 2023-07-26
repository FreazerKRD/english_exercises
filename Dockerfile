FROM python:3.11.4-slim-bookworm

ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY app/ app/

COPY start.sh .

ENV PYTHONPATH=/app

CMD [ "sh", "./start.sh" ]