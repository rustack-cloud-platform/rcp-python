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
    description='Rustack Cloud Platform API Wrapper',
    long_description=long_description,
    url='https://github.com/rustack-cloud-platform/rcp-python',
    download_url='https://github.com/rustack-cloud-platform/rcp-python/tarball/{0}'\
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
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
        ],
    packages=['esu'],
    install_requires=[
        'requests>=2.2.1',
    ],
    extras_require={
        'dev': [
            "responses",
            "yapf==0.30.0",
            "sphinx_rtd_theme==2.0.0",
            "pylint",
            "isort>=5.1.1 ; python_version>='3.6'",
            "tox>=3.9.0",
            "tox-pyenv; platform_system=='darwin'",
            "pytest>=4.6.2",
            "pytest-cov>=2.7.1",
        ]
    },
    python_requires=">=3.4",
)
