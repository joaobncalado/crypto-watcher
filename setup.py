import sys, os
from setuptools import setup

dependencies = ['Pillow', 'numpy', 'RPi', 'spidev', 'requests', 'pytz']

setup(
    name='crypto-watcher',
    description='Crypto Watcher',
    author='João Calado',
    package_dir={'': 'lib'},
    packages=['crypto-watcher'],
    install_requires=dependencies,
)