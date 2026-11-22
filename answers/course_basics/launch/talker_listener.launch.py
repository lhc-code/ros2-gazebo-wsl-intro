import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    config = os.path.join(get_package_share_directory('course_basics'), 'config', 'talker.yaml')
    return LaunchDescription([
        Node(package='course_basics', executable='param_talker', parameters=[config], output='screen'),
        Node(package='course_basics', executable='listener', output='screen'),
    ])
