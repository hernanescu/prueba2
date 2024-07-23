from setuptools import setup, find_packages

# modificamos el setup.py para que lea directamente los requerimientos
with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name='carpinchos',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'}, 
    install_requires=[
        required # Agrega las dependencias del requirements
    ],
)

