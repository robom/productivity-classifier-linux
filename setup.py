from setuptools import setup, find_packages
import shutil
import os
import stat

setup(
    name='unix-productivity-logger',
    version='1.3.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'unix-productivity-logger = logger.__main__:main'
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

# sudo cp productivity-logger /etc/init.d/productivity-logger
# sudo chmod +x /etc/init.d/productivity-logger
