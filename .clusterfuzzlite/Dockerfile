FROM gcr.io/oss-fuzz-base/base-builder-python:v1
RUN apt-get update && apt-get install -y make autoconf automake libtool
COPY . $SRC/source_scan
WORKDIR source_scan
COPY .clusterfuzzlite/build.sh $SRC/
