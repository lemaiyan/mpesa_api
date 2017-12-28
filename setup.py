#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='mpesa-api',
    version='0.1.7',
    packages=find_packages(),
    description="Mpesa B2C, C2B, STKPush Django library based on the new Api's https://developer.safaricom.co.ke",
    author='Jijo Lemaiyan',
    author_email='george@lemaiyan.xyz',
    url='https://github.com/lemaiyan/mpesa_api',
    download_url='https://github.com/lemaiyan/mpesa_api/archive/0.1.7.tar.gz',
    requires=[
        'Django (>=1.11.7)',
        'djangorestframework (>=3.7.3)',
        'celery (>=4.1.0)',
        'requests (>=2.18.4)'
    ],
    include_package_data=True,
    license='MIT License',
    zip_safe=True
)