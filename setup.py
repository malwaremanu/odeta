# setup.py
from setuptools import setup, find_packages

setup(
    name="odeta",
    version="0.1.2",
    author="Manupal Choudhary",
    author_email="tech.manujpr@gmail.com",
    description="A simple NoSQL-like interface for SQLite",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/malwaremanu/odeta",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
