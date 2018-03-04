"""Packaging settings."""
from codecs import open
from os.path import abspath, dirname, join
from subprocess import call
from setuptools import Command, find_packages, setup
from velkozify import __version__


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(['py.test', '--cov=skele', '--cov-report=term-missing'])
        raise SystemExit(errno)


setup(
    name='lol-velkoz-jottings',
    version=__version__,
    description='A tool to inspect and analyse public lol datasets.',
    long_description=long_description,
    url='https://github.com/jameshamm/lol-velkoz-jottings',
    author='James Hamm',
    author_email='',
    license='MIT LICENSE',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5'],
    keywords='cli',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=['Click'],
    extras_require={
        'test': ['coverage', 'pytest', 'pytest-cov']
    },
    entry_points={
        'console_scripts': [
            'velkozify=velkozify.cli:main'
        ]
    },
    cmdclass={'test': RunTests}
)
