# setup.py
from setuptools import setup

setup(
    name='gd',
    version='1.0.0',
    author='Sagi Dana',
    author_email='sagidana1@gmail.com',
    description='library to exploir code',
    long_description=open('README.md').read(),
    url='https://github.com/sagidana/gd',
    packages=['gd'],
    install_requires=[],
    python_requires='>=3.6',
    entry_points = {'console_scripts': "gd=gd:main"},
)
