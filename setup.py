from setuptools import setup
from setuptools import find_packages


VERSION = '0.0.1'

setup(
    name='coroutine',
    url='https://github.com/jschwinger23/coroutine',
    description='Coroutine-based threading interface',
    author='ooth',
    author_email='greyschwinger@gmail.com',
    packages=find_packages(),
    install_requires=[
        'linuxfd>=1.4.4,<2.0.0',
        'pysigset>=0.3.2,<1.0.0',
        'greenlet>=0.4.15,<1.0.0',
    ],
    python_requires='>=3.7.1',
    platform='Linux',
)
