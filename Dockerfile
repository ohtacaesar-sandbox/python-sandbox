FROM python:3.6-alpine

RUN set -eux \
  &&  apk add g++ --no-cache --virtual .build-deps  \
  &&  pip install sklearn requests \
  &&  apk del .build-deps

