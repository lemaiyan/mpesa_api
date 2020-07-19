#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='mpesa-api',
    version='0.2.1',
    packages=find_packages(),
    description="Mpesa B2C, C2B, STKPush Django library based on the new Api's https://developer.safaricom.co.ke",
    author='Jijo Lemaiyan',
    author_email='george@lemaiyan.xyz',
    url='https://github.com/lemaiyan/mpesa_api',
    download_url='https://github.com/lemaiyan/mpesa_api/archive/0.2.1.tar.gz',
    requires=[
        'Django (>=2.1.7)',
        'djangorestframework (>=3.7.3)',
        'celery (>=4.1.0)',
        'requests (>=2.18.4)',
        'decouple (>=3.3)',
        'rangefilter (>=0.6.1)'
    ],
    include_package_data=True,
    license='MIT License',
    zip_safe=True
)