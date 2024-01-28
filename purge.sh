#!/bin/bash
VOLUMES="paperless_pgdata paperless_redisdata"
PAPERLESS_ROOT="/data/paperless-ngx"
DIRS="data media export consume"
ROOT="/home/jk/.local/paperless-ngx"

pushd $ROOT
docker compose down
popd

docker volume rm $VOLUMES
for d in $DIRS; do
	rm -rf $PAPERLESS_ROOT/$d/*
done

pushd $ROOT
docker compose up -d
sleep 5
docker compose run webserver createsuperuser
popd

