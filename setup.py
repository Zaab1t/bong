from setuptools import setup


setup(
    name='bong',
    description='Search Engine written in Python',
    url='https://github.com/Zaab1t/bong',
    author='Carl Bordum Hansen',
    license='MIT',
    packages=['bong'],
    install_requires=['bs4', 'PyStemmer', 'stop_words', 'pymongo']
)
