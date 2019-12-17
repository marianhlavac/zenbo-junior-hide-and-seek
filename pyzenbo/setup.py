from os import path

from setuptools import setup, find_packages

import pyzenbo

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyzenbo',
    version=pyzenbo.__version__,
    description='Python Zenbo junior SDK project',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://zenbo.asus.com/developer/',
    author='ASUSTeK Computer Inc.',
    author_email='zenbodeveloper@asus.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Operating System :: OS Independent",
    ],
    keywords='zenbo',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3.6, <4',
)
