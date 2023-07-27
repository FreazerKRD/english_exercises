#!/bin/sh

set -e

# wait for db
python ./db/wait_for_db.py
python ./db/apply_migrations.py

mkdir -p uploaded_texts
mkdir -p exercises_texts

python -m spacy download en_core_web_sm

exec python main.py