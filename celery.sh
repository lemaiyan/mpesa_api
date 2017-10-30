#!/usr/bin/env bash
celery -A configuration worker -c 5 --loglevel=info