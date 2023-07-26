FROM python:3.11.4-slim

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./scripts /scripts
COPY ./app /app

WORKDIR /app

ENV PYTHONPATH=/app

RUN python -m venv /py && \
  /py/bin/pip install --upgrade pip && \
  /py/bin/pip install -r /tmp/requirements.txt && \
  rm -rf /tmp && \
  chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

CMD [ "start.sh" ]