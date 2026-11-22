from glob import glob

from setuptools import find_packages, setup

package_name = 'course_robot'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/config', glob('config/*.yaml')),
        ('share/' + package_name + '/urdf', glob('urdf/*')),
        ('share/' + package_name + '/worlds', glob('worlds/*.sdf')),
        ('share/' + package_name + '/rviz', glob('rviz/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Haechan Lee',
    maintainer_email='lhc-code@users.noreply.github.com',
    description='2륜 이동 로봇 URDF, Gazebo Harmonic 시뮬레이션, 1m 이동 node',
    license='MIT',
    entry_points={
        'console_scripts': [
            'move_1m = course_robot.move_1m:main',
        ],
    },
)
