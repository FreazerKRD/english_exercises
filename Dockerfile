FROM python:3.11.4-alpine3.18 

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./scripts /scripts
COPY ./app /app

WORKDIR /app

ENV PYTHONPATH=/app

ARG DEV=false
RUN apk add --no-cache --virtual .build-deps \
      gcc \
      gfortran \
      g++ \
      musl-dev \
      python3-dev \
      libc-dev \
      libffi-dev \
      openssl-dev \
      make \
      openblas-dev && \
    apk add --no-cache \
      libstdc++ \
      openblas && \
    python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install --no-cache-dir -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
    then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    apk del .build-deps && \
    rm -rf /tmp && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

CMD [ "start.sh" ]