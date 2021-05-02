from setuptools import setup, find_packages

setup(
    name="dante-tokenizer",
    version="0.1",
    author="Emanuel Huber",
    author_email="emanuel.huber@usp.br",
    packages=find_packages(),
    license="Apache 2.0",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/huberemanuel/twitter-portuguese-tokenizer",
    download_url="https://github.com/huberemanuel/twitter-portuguese-tokenizer/archive/refs/tags/v0.1-alpha.tar.gz",
    keywords=["tokenizer", "twitter", "portuguese"],
    install_requires=[
        "nltk>=3.6.2",
        "regex>=2021.4.4"
    ],
    classifier=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers|Researchers",
        "Topic :: Natural Language Processing :: Tokenizer",
        "License :: OSI Approved :: Apache 2.0",
        "Programming Language :: Python :: 3.8"
    ]
)