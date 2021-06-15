#!/usr/bin/env bash
python3 init_db.py && uwsgi --module "wsgi:app" --master --processes 2 --threads 2 --http :9090 --vacuum

