#!/usr/bin/env bash

gunicorn3 wsgi:app --bind 0.0.0.0:8080 --log-level=debug --workers=4
