import os

from setuptools import setup, find_packages


setup(
    name='Akdanda Quantum User API',
    version='0.1.0',
    description='OpenStack L3 User-Facing REST API',
    author='DreamHost',
    author_email='dev-community@dreamhost.com',
    url='http://github.com/dreamhost/akanda',
    license='BSD',
    install_requires=[
    ],
    namespace_packages=['akanda'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
