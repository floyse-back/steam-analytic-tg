#!/usr/bin/env bash

if [ "$RUN_PRESTANT" == "1" ];then
  set -e

  echo "Run apply migrations.."
  sleep 30
  alembic upgrade head
  sleep 25
  echo "Migrations applied!"
fi

sleep 22

exec "$@"
