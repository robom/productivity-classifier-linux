from setuptools import setup, find_packages
import shutil
import os
import stat
import platform

if any(platform.win32_ver()):
    requires = [
        "requests",
        # "pyHook-1.5.1-cp35-none-win_amd64.whl--no-index "
    ]
else:
    requires = [
        "requests",
        "python3-xlib",
    ]

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
    install_requires=requires,
)



# sudo cp productivity-logger /etc/init.d/productivity-logger
# sudo chmod +x /etc/init.d/productivity-logger
