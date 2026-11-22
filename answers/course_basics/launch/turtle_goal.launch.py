from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    goal_x = LaunchConfiguration('goal_x')
    goal_y = LaunchConfiguration('goal_y')
    return LaunchDescription([
        DeclareLaunchArgument('goal_x', default_value='8.0'),
        DeclareLaunchArgument('goal_y', default_value='8.0'),
        Node(package='turtlesim', executable='turtlesim_node'),
        Node(
            package='course_basics',
            executable='turtle_goal',
            parameters=[{'goal_x': goal_x, 'goal_y': goal_y}],
            output='screen',
        ),
    ])
