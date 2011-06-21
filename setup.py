import distribute_setup
distribute_setup.use_setuptools()
from setuptools import setup, find_packages

setup(
    name = "Wicked Jukebox Database",
    version = "1.0",
    packages = find_packages(),

    install_requires = [
        'sqlalchemy==0.7',
    ],

)
