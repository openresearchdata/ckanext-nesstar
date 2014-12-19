from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
    name='ckanext-nesstar',
    version=version,
    description="NESSTAR/OAI-PMH  Harvester for CKAN",
    long_description="",
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Liip AG',
    author_email='ogd@liip.ch',
    url='http://www.liip.ch',
    license='AGPL',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.nesstar'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
        'ckanext-oaipmh'
    ],
    entry_points=\
    """
    [ckan.plugins]
    nesstar_harvester=ckanext.nesstar.harvester:NesstarHarvester
    [paste.paster_command]
    harvester=ckanext.nesstar.command:NesstarHarvesterCommand
    """,
)
