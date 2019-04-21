from setuptools import setup
from setuptools import find_packages


VERSION = '0.0.1'

setup(
    name='coroutine',
    url='https://github.com/jschwinger23/coroutine',
    description='Coroutine-based threading interface',
    author='ooth',
    author_email='greychwinger@gmail.com',
    packages=find_packages(),
    install_requires=[
        'linuxfd',
        'pysigset',
        'greenlet>=0.4.15,<1.0.0',
    ],
    python_requires='>=3.7.1',
    platform='Linux',
)
