import setuptools

from automx2 import IDENTIFIER
from automx2 import VERSION

with open('README.md', 'r') as f:
    readme = f.read()

setuptools.setup(
    name=IDENTIFIER,
    version=VERSION,
    author='Ralph Seichter',
    author_email='s@sys4.de',
    description='Mail client autoconfiguration service',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://automx.org/',
    project_urls={
        'Source': 'https://gitlab.com/automx/automx2',
        'Tracker': 'https://gitlab.com/automx/automx2/issues',
    },
    packages=setuptools.find_packages(),
    data_files=[
        ('scripts', ['contrib/flask.sh']),
        ('scripts', ['contrib/setupvenv.sh']),
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'Flask>=1.1.1',
        'Flask-Migrate>=2.5.2',
        'Flask-SQLAlchemy>=2.4.1',
    ],
    python_requires='>=3.7',
)
