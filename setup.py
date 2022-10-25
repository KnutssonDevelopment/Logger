from setuptools import setup, find_packages

setup(
    name='Logger',
    version='1.0.1',
    description='A simple logging module that will write to a file and to the console.',
    author='Brian F. Knutsson',
    author_email='<development@knutsson.it>',
    url='https://github.com/KnutssonDevelopment/Logger',
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Development Status :: 2 - Testing",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    packages=find_packages(),
    include_package_data=True
)
