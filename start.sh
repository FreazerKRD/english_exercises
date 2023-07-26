#!/bin/sh

set -e

cd ./app
mkdir uploaded_texts
mkdir exercises_texts

python -m spacy download en_core_web_sm

exec python main.py