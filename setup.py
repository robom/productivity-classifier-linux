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
    version='1.3.4',
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



# python3 setup.py --command-packages=stdeb.command bdist_deb
# cp productivity-logger deb_dist/unix-productivity-logger-
# cd deb_dist/unix-productivity-logger-
# add to rules:
# sudo cp productivity-logger /etc/init.d/productivity-logger
# sudo chmod +x /etc/init.d/productivity-logger
# dpkg-source --commit
# sudo dpkg-buildpackage -rfakeroot -uc -us
# sudo apt-get remove python3-unix-productivity-logger
# cd ..
# sudo dpkg -i python3-unix-productivity-logger_
# https://pypi.python.org/pypi/stdeb/0.8.5
# sudo python3 setup.py install --record files.txt
