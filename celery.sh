#!/usr/bin/env bash
celery -A configuration worker -c 5 --loglevel=info -Q b2c_result,b2c_request,celery