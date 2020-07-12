#!/usr/bin/env bash
celery -A config worker -c 5 --loglevel=info -Q b2c_result,b2c_request,celery,c2b_confirmation,c2b_validation,online_checkout_request,online_checkout_callback