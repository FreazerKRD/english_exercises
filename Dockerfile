FROM python:3.11.4-slim-bookworm

ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
COPY ./app /app
COPY start.sh .

RUN pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x start.sh

WORKDIR /app

ENV PYTHONPATH=/app
CMD [ "./start.sh" ]