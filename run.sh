#!/bin/bash
docker run \
  --rm \
  --platform linux/amd64 \
  -p 8888:8888 \
  -e JUPYTER_ENABLE_LAB=yes \
  -e SCORE_OUTPUT_FORMAT=html \
  -e GRADING_API_URL=http://gateway.docker.internal:2400 \
  -v "${PWD}":/home/jovyan/work worldquant/mscfe:fd