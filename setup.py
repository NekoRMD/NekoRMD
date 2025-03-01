from setuptools import setup, find_packages

setup(
    name='NekoRMD',
    version='0.2.2',
    author='Artem-Darius Weber',
    author_email='neko-rmd@k-lab.su',
    description='NekoRMD is a Python library for controlling RMD series motors through a CAN interface. It provides a wide range of functions for motor control and monitoring.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/NekoRMD/NekoRMD',
    packages=find_packages(),
    install_requires=[
        "python-can",
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
