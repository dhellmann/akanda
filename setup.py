from setuptools import setup, find_packages

from akanda import meta
from akanda.utils import dist


setup(
    name=meta.display_name,
    version=meta.version,
    description=meta.description,
    author=meta.author,
    author_email=meta.author_email,
    url=meta.url,
    license=meta.license,
    packages=find_packages() + ["twisted.plugins"],
    package_data={
        "twisted": ['plugins/restapi.py']
        },  
    install_requires=meta.requires,
    zip_safe=False,
    #entry_points={
    #    'console_scripts': [
    #        'akanda-configure-ssh ='
    #        'akanda.tools.management:configure_ssh',
    #    ]
    #},
)

dist.refresh_plugin_cache()
