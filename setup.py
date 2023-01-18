from setuptools import setup, find_packages

required = []
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='ctrls',
    version='0.1.0',
    py_modules=['ctrls'],
    install_requires=required,
    entry_points={
        'console_scripts': [
            'ctrls=ctrls:cli',
        ],
    },
)
