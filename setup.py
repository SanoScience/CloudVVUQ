from setuptools import find_packages, setup

setup(
    name='cloudvvuq',
    packages=find_packages(),
    version='0.1.0',
    description='Run simulations on cloud with EasyVVUQ functionality ',
    install_requires=['easyvvuq', 'backoff', 'aiohttp', 'tqdm', 'google-cloud-storage', 'mkdocs-material']
)
