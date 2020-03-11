
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path, environ

here = path.abspath(path.dirname(__file__))
build_version = environ.get('build_version', '0.0.0')

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='foundations-gcp',
    version=build_version,
    description='A tool for machine learning development',
    classifiers=[ 
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
    ],
    install_requires=[
        'google-api-python-client==1.7.3',
        'google-auth-httplib2==0.0.3',
        'google-cloud-storage==1.10.0',
        'foundations-contrib=={}'.format(build_version)
    ],
    packages=find_packages('src'),
    package_dir={'':'src'},
    package_data={
        'foundations_gcp': ['resources/*', 'licenses/*/*'],
    }
)