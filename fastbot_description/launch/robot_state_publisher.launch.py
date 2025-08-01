import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro

from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.actions import OpaqueFunction


def launch_setup(context, *args, **kwargs):
    robot_name = LaunchConfiguration("robot_name").perform(context)
    robot_file = LaunchConfiguration("robot_file").perform(context)

    # Topic and node names
    robot_description_topic_name = f"/{robot_name}_robot_description"
    robot_state_publisher_name = f"{robot_name}_robot_state_publisher"
    joint_state_topic_name = f"/{robot_name}/joint_states"

    package_description = "fastbot_description"

    # Get URDF/Xacro path
    robot_desc_path = os.path.join(
        get_package_share_directory(package_description), "onshape", robot_file
    )

    # Process Xacro file with arguments
    robot_desc = xacro.process_file(robot_desc_path, mappings={"robot_name": robot_name})
    xml = robot_desc.toxml()

    # Define robot_state_publisher node (no use_sim_time)
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name=robot_state_publisher_name,
        emulate_tty=True,  # Optional: better log display
        parameters=[{"robot_description": xml}],
        remappings=[
            ("/robot_description", robot_description_topic_name),
            ("/joint_states", joint_state_topic_name),
        ],
        output="screen",
    )
    js = Node(            package='joint_state_publisher',            executable='joint_state_publisher',            name='joint_state_publisher',        )
    static_tf_pub_node = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="static_tf_pub_wheel",
        arguments=["0", "0", "0", "0", "0", "0", "base_link", "wheel_d65x25_v1"],
        output="screen"
    )
    static_tf_pub_node2 = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="static_tf_pub_wheel",
        arguments=["0", "0", "0", "0", "0", "0", "base_link", "wheel_d65x25_v1_2"],
        output="screen"
    )

    return [robot_state_publisher_node]


def generate_launch_description():
    robot_name_arg = DeclareLaunchArgument("robot_name", default_value="fastbot")
    robot_file_arg = DeclareLaunchArgument("robot_file", default_value="robot.urdf")

    return LaunchDescription([
        robot_name_arg,
        robot_file_arg,
        OpaqueFunction(function=launch_setup)
    ])
