from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='rpicard',
      version=version,
      description="A daemon with a web interface to control a raspberry pi car",
      long_description=\
"""
To be described.
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='RaspberryPi Car',
      author='fortime',
      author_email='palfortime@gmail.com',
      url='To be xxx',
      license='MIT License',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
