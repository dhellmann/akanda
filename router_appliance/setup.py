import os

from setuptools import setup, find_packages


setup(
    name='akanda-router',
    version='0.1.0',
    description='A packet filter based router appliance',
    author='DreamHost',
    author_email='dev-community@dreamhost.com',
    url='http://github.com/dreamhost/akanda',
    license='BSD',
    install_requires=[
        'flask>=0.9',
        'gunicorn>=0.14.6',
        'netaddr>=0.7.7',
    ],
    namespace_packages=['akanda'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'akanda-configure-ssh ='
            'akanda.router.commands.management:configure_ssh',
            'akanda-configure-gunicorn = '
            'akanda.router.commands.management:configure_gunicorn',
            'akanda-api-dev-server =akanda.router.api.server:main',
        ]
    },
)
