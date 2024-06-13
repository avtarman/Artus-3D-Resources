from setuptools import setup, find_packages

setup(
    name='ArtusAPI',
    version='0.5.0',
    description='API to control Artus Family of Robots by Sarcomere Dynamics Inc',
    # package_dir={'': '/'},  # tells setuptools that your packages are under src
    packages=find_packages(exclude=['data*', 'examples*', 'tests*','venv*']),
    author='Sarcomere Dynamics Inc.'
    # packages=find_packages(where='/'),
    # other setup configurations
)