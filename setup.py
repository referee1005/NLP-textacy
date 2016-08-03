import io
import os

from setuptools import setup, find_packages


def read_file(fname, encoding='utf-8'):
    path = os.path.join(os.path.dirname(__file__), fname)
    return io.open(path, encoding=encoding).read()


setup(
    name='textacy',
    version='0.2.8',
    description='Higher-level text processing, built on spaCy',
    long_description=read_file('README.rst'),

    url='https://github.com/chartbeat-labs/textacy',
    download_url='https://pypi.python.org/pypi/textacy',

    author='Burton DeWilde',
    author_email='burtdewilde@gmail.com',
    license='Apache',

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Natural Language :: English',
        'Topic :: Text Processing :: Linguistic',
        ],
    keywords='textacy, spacy, nlp, text processing, linguistics',

    packages=find_packages(),
    install_requires=[
        'backports.lzma>=0.0.6',
        'cachetools',
        'cld2-cffi',
        'cytoolz',
        'ftfy',
        'fuzzywuzzy',
        'gensim',
        'ijson',
        'matplotlib',
        'networkx',
        'numpy>=1.8.0',
        'pyemd>=0.3.0',
        'pyphen',
        'python-levenshtein>=0.12.0',
        'requests>=2.10.0',
        'scipy',
        'scikit-learn',
        'spacy>=0.101.0',
        'unidecode',
        ],
    )
