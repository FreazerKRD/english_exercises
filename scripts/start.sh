#!/bin/sh

set -e

mkdir -p uploaded_texts
mkdir -p exercises_texts

python -m spacy download en_core_web_sm

exec python main.app