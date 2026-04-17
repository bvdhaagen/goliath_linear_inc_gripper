from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.conditions import IfCondition
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution, LaunchConfiguration

from launch_ros.actions import Node, PushRosNamespace
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    declared_arguments = [
        DeclareLaunchArgument(
            "namespace",
            default_value="robot_1",
            description="Namespace for the robot (top line of the yaml must match)",
        ),
        DeclareLaunchArgument(
            "gui",
            default_value="false",
            description="Start RViz2 automatically",
        ),
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="false",
            description="Use simulation time",
        ),
    ]

    namespace = LaunchConfiguration("namespace")
    use_sim_time = LaunchConfiguration("use_sim_time")
    gui = LaunchConfiguration("gui")

        # ✅ Modified: Pass namespace to xacro
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [
                    FindPackageShare("goliath_controller"),
                    "urdf",
                    "goliath_ns.urdf.xacro",
                ]
            ),
            " ",
            "namespace:=", namespace,  # Pass namespace to xacro
            " ",
            "use_sim_time:=", use_sim_time,
        ]
    )

    robot_description = {"robot_description": robot_description_content, "use_sim_time": use_sim_time}
    # Robot state publisher node (standalone zonder namespace check)
    robot_state_pub_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        namespace=namespace,
        output="both",
        parameters=[robot_description],
    )

    # RViz config file
    rviz_config_file = PathJoinSubstitution(
        [
            FindPackageShare("goliath_controller"),
            "rviz",
            "view_robot.rviz",
        ]
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        namespace=namespace,
        output="log",
        arguments=["-d", rviz_config_file],
        condition=IfCondition(gui),
    )

    return LaunchDescription(
        declared_arguments +
        [
            robot_state_pub_node,
            rviz_node,
        ]
    )
