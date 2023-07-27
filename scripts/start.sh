#!/bin/sh

set -e

# wait for db
python wait_for_db.py

mkdir -p uploaded_texts
mkdir -p exercises_texts

python -m spacy download en_core_web_sm

exec python main.py