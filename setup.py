from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='walmart-calendar',
    version='1.1.0',
    description='Micro library for performing data calculations with Walmart\'s 4-5-4 retail calendar',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/merchantlabs/walmart-calendar',
    author='Merchant Labs',
    author_email='support@merchantlabs.io',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords='data-analytics calendar bi',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    extras_require={
    'test': ['pytest'],
    },
)
