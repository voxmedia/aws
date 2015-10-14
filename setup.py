# coding: utf-8

from setuptools import setup, find_packages

setup(
        name = 'tc_aws',
        version = "1.1.1",
        description = 'Thumbor AWS extensions',
        author = 'William King, et al',
        author_email = 'willtrking@gmail.com',
        zip_safe = False,
        include_package_data = True,
        packages=find_packages(),
        requires=['python-dateutil','thumbor','boto']
)
