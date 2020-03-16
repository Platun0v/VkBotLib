#!/usr/bin/env python
from setuptools import setup
from io import open

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(name='VkBotLib',
      version='0.4.2',

      author='Platun0v',
      author_email='platun0v@protonmail.com',
      url='https://github.com/platun0v/vk_bot',

      description='Python Vk bot api',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='Apache License, Version 2.0',
      keywords='vk bot api tools',

      packages=['vk_bot'],
      install_requires=['requests', 'vk_api'],

      classifiers=[
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'License :: OSI Approved :: Apache Software License',
      ]
      )
