#!/bin/bash
python manage.py migrate --noinput
gunicorn -b :$PORT myproject.wsgi