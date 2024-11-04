from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'artuslite_ros_api'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Include launch files
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        # Include config files if needed
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml'))
    ],
    install_requires=['setuptools',
                      'ArtusAPI',
                      'pyserial'],
    zip_safe=True,
    maintainer='gagan',
    maintainer_email='gagandeep@sarcomeredynamics.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'artuslite_ros_node = artuslite_ros_api.artuslite_ros_api:main',
        ],
    },
)
