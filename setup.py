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
        install_requires=['python-dateutil','thumbor>=5.1.0,<5.2.0','boto']
)
