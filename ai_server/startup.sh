#!/usr/bin/env bash
set -e

mkdir -p temp
mkdir -p cache
mkdir -p weights

uvicorn main:app --host 0.0.0.0 --port ${PORT:-7860}
