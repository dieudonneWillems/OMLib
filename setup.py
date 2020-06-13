import sys

from setuptools import setup, find_packages

setup(
    name='omlib',
    version='0.0.1',
    description='Python library to work with the Ontology of Units of Measure',
    long_description=open('README.md').read(),
    author='Don Willems',
    author_email='user@exampledomain.com',
    zip_safe=True,
    url='https://github.com/lapsedPacifist/OMLib',
    license='GNU3.0',
    packages=find_packages(),
    install_requires=['rdflib']
    tests_require=["pytest"])
