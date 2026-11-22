# Gazebo Harmonic에 simple_bot 불러오기
#   ros2 launch course_robot gazebo.launch.py
#   ros2 launch course_robot gazebo.launch.py render_engine:=ogre   (화면이 검을 때)
#   ros2 launch course_robot gazebo.launch.py use_camera:=true      (카메라 추가)
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    share = get_package_share_directory('course_robot')
    xacro_file = os.path.join(share, 'urdf', 'simple_bot.urdf.xacro')
    world_file = os.path.join(share, 'worlds', 'course.sdf')
    bridge_file = os.path.join(share, 'config', 'bridge.yaml')
    bridge_camera_file = os.path.join(share, 'config', 'bridge_camera.yaml')
    rviz_file = os.path.join(share, 'rviz', 'simple_bot.rviz')

    use_camera = LaunchConfiguration('use_camera')
    render_engine = LaunchConfiguration('render_engine')
    rviz = LaunchConfiguration('rviz')

    robot_description = ParameterValue(
        Command(['xacro ', xacro_file, ' use_camera:=', use_camera]), value_type=str)

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')),
        launch_arguments={
            'gz_args': ['-r -v 1 --render-engine ', render_engine, ' ', world_file],
        }.items(),
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description, 'use_sim_time': True}],
    )

    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description', '-name', 'simple_bot', '-z', '0.02'],
        output='screen',
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{'config_file': bridge_file, 'use_sim_time': True}],
        output='screen',
    )

    bridge_camera = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='camera_bridge',
        parameters=[{'config_file': bridge_camera_file, 'use_sim_time': True}],
        condition=IfCondition(use_camera),
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_file],
        parameters=[{'use_sim_time': True}],
        condition=IfCondition(rviz),
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_camera', default_value='false'),
        DeclareLaunchArgument('render_engine', default_value='ogre2', description='ogre2 또는 ogre'),
        DeclareLaunchArgument('rviz', default_value='false'),
        gz_sim,
        robot_state_publisher,
        spawn,
        bridge,
        bridge_camera,
        rviz_node,
    ])
