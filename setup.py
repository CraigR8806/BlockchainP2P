from setuptools import setup, find_packages

setup(
   name='BlockchainP2P',
   version='0.0.1',
   description='A Peer 2 Peer network implementation to support a blockchain ecosystem',
   author='Craig Rmaage',
   author_email='',
   packages=find_packages(exclude=['test']),
   install_requires=['wheel', 'flask', 'requests', 'pycryptodome', 'jsonpickle'], 
)