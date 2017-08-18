#!/usr/bin/env python3

from setuptools import setup

setup(name='junko',
      version='0.1.0',
      description='APIGateway-Lambda website framework.',
      author='Steve Norum',
      author_email='stevenorum@gmail.com',
      url='www.stevenorum.com',
      packages=['junko'],
      package_dir={'junko': 'junko'},
      test_suite='tests',
     )
