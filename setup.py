from setuptools import setup, find_packages

setup(
    name='unix-productivity-logger',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'linuxlogger3 = logger.__main__:main'
        ],
    },
    url='',
    license='GNU General Public License, version 2',
    author='lubomir.vnenk',
    author_email='lubomir.vnenk@zoho.com',
    description='',
    install_requires=[
        "requests",
        "python3-xlib"
    ],
)
