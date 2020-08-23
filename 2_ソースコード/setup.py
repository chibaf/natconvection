
import ast
import os
import re
import subprocess
from glob import glob

from setuptools import Command, setup

PACKAGE_NAME = 'table_top_loop'


class SimpleCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


class TestCommand(SimpleCommand):
    def run(self):
        subprocess.check_call(['pytest'])


class VetCommand(SimpleCommand):
    def run(self):
        subprocess.check_call(['flake8'])


class FmtCommand(SimpleCommand):
    def run(self):
        # isort
        subprocess.call(['isort', '-y'])
        # pyformat
        fmttarg = glob(f'{PACKAGE_NAME}/**/*.py', recursive=True)
        fmttarg.append('setup.py')
        for f in fmttarg:
            print(f)
            subprocess.call(['pyformat ', '--in-place', f])


setup(
    cmdclass={
        'pyt': TestCommand,
        'vet': VetCommand,
        'fmt': FmtCommand
    },
)
