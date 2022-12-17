import gym as gym
from setuptools import setup

setup(
    name='alpaca_gym',
    version='0.1',
    packages=[''],
    url='',
    license='apache-2',
    author='Hytham Alobydi',
    author_email='',
    description='Gym environments for alpaca trading service',
    install_requires=[
        'gym==0.13.0',
        'alpaca-trade-api'
    ]
)
