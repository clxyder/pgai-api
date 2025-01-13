#!/bin/sh

gunicorn --worker-class uvicorn.workers.UvicornWorker -w 4 -b :8000 "app:create_app()"
