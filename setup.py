# setup.py
from setuptools import setup, find_packages

setup(
    name='gd',
    version='1.0.0',
    author='Sagi Dana',
    author_email='sagidana1@gmail.com',
    description='library to exploir code',
    long_description=open('README.md').read(),
    url='https://github.com/sagidana/gd',
    packages = find_packages(),
    include_package_data=True,
    install_requires = [open("requirements.txt", "r", encoding="utf-8").read()],
    python_requires='>=3.6',
    entry_points = {'console_scripts': "gd=gd:main"},
)



