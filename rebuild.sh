#!/bin/bash
ROOT=/home/jk/.local/paperless-ngx
FILE=docker-compose.yml
IMPORTER=/home/jk/.local/paperless_import
PR=/data/paperless-ngx
set -e

docker build --network host --tag paperless:local .
pushd $ROOT
docker compose --file $FILE down
if [ -n "$1" ]; then
	echo removing previous data...
	rm -rf $PR/consume/* $PR/data/* $PR/media/* $PR/export/*
fi
pushd $IMPORTER
. .venv/bin/activate
#python import_pcloud.py /mnt/pcloud/Dokumente
popd
docker compose --file $FILE up -d
popd
