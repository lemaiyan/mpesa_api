#!/usr/bin/env bash
set -e
python manage.py migrate --noinput

#python property_manager.py collectstatic —-noinput
# first remove the collect static folder
rm -rf static
echo yes | python manage.py collectstatic

#python property_manager.py runserver 0.0.0.0:80
exec gunicorn --bind=0.0.0.0:80 config.wsgi --workers=5 --log-level=info --log-file=---access-logfile=- --error-logfile=- --timeout 30000 --reload