#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='mpesa-api',
    version='0.1',
    packages=find_packages(),
    description='Mpesa B2C, C2B, Online Checkout api for Django',
    author='Jijo Lemaiyan',
    author_email='george@lemaiyan.xyz',
    url='https://bitbucket.org/lemaiyan/mpesa_api',
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