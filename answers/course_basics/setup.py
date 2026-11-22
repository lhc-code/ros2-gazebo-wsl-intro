from glob import glob

from setuptools import find_packages, setup

package_name = 'course_basics'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/config', glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Haechan Lee',
    maintainer_email='lhc-code@users.noreply.github.com',
    description='ROS2 기초 실습 정답 코드',
    license='MIT',
    entry_points={
        'console_scripts': [
            'talker = course_basics.talker:main',
            'listener = course_basics.listener:main',
            'add_server = course_basics.add_server:main',
            'add_client = course_basics.add_client:main',
            'param_talker = course_basics.param_talker:main',
            'turtle_goal = course_basics.turtle_goal:main',
        ],
    },
)
