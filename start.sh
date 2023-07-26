#!/bin/sh

set -e

cd ./app

python -m spacy download en_core_web_sm

exec python main.py