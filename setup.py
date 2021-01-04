import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('esu/__init__.py', 'r', encoding='utf-8') as file:
    regex_version = r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]'
    version = re.search(regex_version, file.read(), re.MULTILINE).group(1)

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rustack-esu',
    version=version,
    description='RUSTACK-ESU Cloud API Wrapper',
    long_description=long_description,
    url='https://github.com/pilat/rustack-esu',
    download_url='https://github.com/pilat/rustack-esu/tarball/{0}'\
        .format(version),
    author='Vladimir K Urushev',
    author_email='urushev@yandex.ru',
    maintainer='Vladimir K Urushev',
    maintainer_email='urushev@yandex.ru',
    keywords=['cloud', 'api'],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        ],
    packages=['esu'],
    install_requires=[
        'requests>=2.2.1',
    ],
    extras_require={
        'dev': [
            # "black>=19.10b0 ; python_version>='3.6'",
            "responses",
            "yapf==0.30.0",
            "codecov>=2.0.15",
            # "colorama>=0.3.4",
            "pylint",
            "isort>=5.1.1 ; python_version>='3.6'",
            "tox>=3.9.0",
            "tox-pyenv",  # osx
            # "tox-travis>=0.12",
            "pytest>=4.6.2",
            "pytest-cov>=2.7.1",
            # "Sphinx>=2.2.1",
            # "sphinx-autobuild>=0.7.1 ; python_version>='3.6'",
            # "sphinx-rtd-theme>=0.4.3",
        ]
    },
    python_requires=">=3.4",
)
