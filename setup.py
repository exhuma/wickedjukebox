import distribute_setup
distribute_setup.use_setuptools()
from setuptools import setup, find_packages

setup(
    name = "Wicked Jukebox Database",
    version = "1.0",
    license = "BSD 3-Clause",
    packages = find_packages(),
    long_description=open("README.rst").read(),

    install_requires = [
        'sqlalchemy==0.7',
    ],

)
