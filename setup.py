"""
Copyright © 2019-2021 Ralph Seichter

This file is part of automx2.

automx2 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

automx2 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with automx2. If not, see <https://www.gnu.org/licenses/>.
"""
import setuptools

from automx2 import IDENTIFIER
from automx2 import VERSION

with open('README.md', 'r') as f:
    readme = f.read()

setuptools.setup(
    name=IDENTIFIER,
    version=VERSION,
    author='Ralph Seichter',
    author_email='automx2@seichter.de',
    description='Mail client autoconfiguration service',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://rseichter.github.io/automx2/',
    project_urls={
        'Source': 'https://github.com/rseichter/automx2',
        'Tracker': 'https://github.com/rseichter/automx2/issues',
    },
    packages=setuptools.find_packages(),
    data_files=[
        ('scripts', ['contrib/flask.sh']),
        ('scripts', ['contrib/setupvenv.sh']),
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'Flask>=1.1.1',
        'Flask-Migrate>=2.5.2',
        'Flask-SQLAlchemy>=2.4.1',
        'ldap3>=2.6',
    ],
    python_requires='>=3.7',
)
