from glob import glob
from os.path import basename, splitext
from setuptools import find_packages, setup

setup(
    name='libraries',
    version='0.1',
    packages=find_packages(where='libraries'),
    package_dir={'': 'libraries'},
    py_modules=[splitext(basename(path))[0] for path in glob('emulate/*.py')],
    description='Uses odeint and solve_ivp to solve differential equations',
    author='Alberto J. Garcia',
    author_email='garcia.823@osu.edu',
    zip_safe=False
)
