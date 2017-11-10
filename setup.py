#!/usr/bin/env python3

from setuptools import setup
import tenzing

setup(name='junko',
      version='1.0.1',
      description='APIGateway-Lambda website framework.',
      author='Steve Norum',
      author_email='stevenorum@gmail.com',
      url='www.stevenorum.com',
      packages=['junko'],
      package_dir={'junko': 'junko'},
      test_suite='tests',
      cmdclass = {'upload':tenzing.Upload},
      install_requires = ['jinja2','calvin']
)
