import os
import yaml
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import ExecuteProcess, RegisterEventHandler
from ament_index_python.packages import get_package_share_directory, get_package_prefix
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
import xacro
from launch_ros.substitutions import FindPackageShare
from moveit_configs_utils import MoveItConfigsBuilder
from launch.event_handlers import OnProcessExit

def load_file(package_name, file_path):
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, file_path)

    try:
        with open(absolute_file_path, "r") as file:
            return file.read()
    except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        return None


def load_yaml(package_name, file_path):
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, file_path)

    try:
        with open(absolute_file_path, "r") as file:
            return yaml.safe_load(file)
    except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        return None

def load_xacro(file_path, mappings: dict = None):
    # raise_if_file_not_found(file_path)
    file = xacro.process_file(file_path, mappings=mappings)
    return file.toxml()
def generate_launch_description():

    # Command-line arguments
    tutorial_arg = DeclareLaunchArgument(
        "rviz_tutorial", default_value="False", description="Tutorial flag"
    )
    moveit_config = ( MoveItConfigsBuilder("welding_robot", package_name="Robot_ver2")
                     .trajectory_execution(file_path="config/welding.yaml")
                     .to_moveit_configs())

    robot_description = moveit_config.robot_description


    robot_description_semantic_config = load_file(
        "Robot_ver2", "config/welding_robot.srdf"
    )
    robot_description_semantic = {
        "robot_description_semantic": robot_description_semantic_config
    }

    kinematics_yaml = load_yaml(
        "Robot_ver2", "config/kinematics.yaml"
    )
    robot_description_kinematics = {"robot_description_kinematics": kinematics_yaml}

    # # Planning Functionality
    # ompl_planning_pipeline_config = {
    #     "move_group": {
    #         "planning_plugin": "ompl_interface/OMPLPlanner",
    #         "request_adapters": """default_planner_request_adapters/AddTimeOptimalParameterization default_planner_request_adapters/FixWorkspaceBounds default_planner_request_adapters/FixStartStateBounds default_planner_request_adapters/FixStartStateCollision default_planner_request_adapters/FixStartStatePathConstraints""",
    #         "start_state_max_bounds_error": 0.1,
    #     }
    # }
    # ompl_planning_yaml = load_yaml(
    #     "movelt_sim", "config/ompl_planning.yaml"
    # )
    # ompl_planning_pipeline_config["move_group"].update(ompl_planning_yaml)

    #Trajectory Execution Functionality
    moveit_simple_controllers_yaml = load_yaml(
        "Robot_ver2", "config/welding.yaml"
    )
    # moveit_simple_controllers_yaml = load_yaml(
    #     "moveit_resources_panda_moveit_config", "config/panda_controllers.yaml"
    # )
    moveit_controllers = {
        "moveit_simple_controller_manager": moveit_simple_controllers_yaml,
        # "moveit_controller_manager": "moveit_simple_controller_manager/MoveItSimpleControllerManager",
    }

    trajectory_execution = {
        "moveit_manage_controllers": True,
        "trajectory_execution.allowed_execution_duration_scaling": 1.2,
        "trajectory_execution.allowed_goal_duration_margin": 0.5,
        "trajectory_execution.allowed_start_tolerance": 0.01,
    }

    planning_scene_monitor_parameters = {
        "publish_planning_scene": True,
        "publish_geometry_updates": True,
        "publish_state_updates": True,
        "publish_transforms_updates": True,
    }

    # Start the actual move_group node/action server
    run_move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            robot_description,
            robot_description_semantic,
            kinematics_yaml,
            # # ompl_planning_pipeline_config,
            trajectory_execution,
            moveit_controllers,
            planning_scene_monitor_parameters,
             {"use_sim_time": True},
            moveit_config.to_dict()
        ],
    )

    # RViz
    # tutorial_mode = LaunchConfiguration("rviz_tutorial")
    # rviz_base = LaunchConfiguration("rviz_config")
    rviz_base = os.path.join(get_package_share_directory("Robot_ver2"), "config")
    rviz_full_config = os.path.join(rviz_base, "moveit.rviz")
    # rviz_empty_config = os.path.join(rviz_base, "moveit.rviz")

    rviz_node_tutorial = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_full_config],
        parameters=[
            robot_description,
            robot_description_semantic,
            # ompl_planning_pipeline_config,
            kinematics_yaml,
        ],
        # condition=IfCondition(tutorial_mode),
    )
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_full_config],
        parameters=[
            robot_description,
            robot_description_semantic,
            # ompl_planning_pipeline_config,
            kinematics_yaml,
             {"use_sim_time": True},
        ],
        # condition=UnlessCondition(tutorial_mode),
    )

    # Static TF
    static_tf = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="static_transform_publisher",
        output="log",
        arguments=["0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "world", "link_1"],
    )

    # Publish TF
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="both",
        parameters=[robot_description, {"use_sim_time": True}],
    )

    # ros2_control using FakeSystem as hardware
    ros2_controllers_path = os.path.join(
        get_package_share_directory("Robot_ver2"),        
        "config/ros2_controllers.yaml",
    )

    ros2_control_node = Node(        
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            moveit_config.robot_description,
            str(moveit_config.package_path / "config/ros2_controllers.yaml"),
        ],
        output="both",
    )


    #Load controllers
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
        ],
    )

    arm_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["arm_controller", 
            "--controller-manager",
            "/controller_manager",
        ],
    )

    ### Gazebo ###
    
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
             )
    Model_Robot_description_dir = get_package_share_directory('Model_Robot')
    Model_Robot_description_share = os.path.join(get_package_prefix('Model_Robot'), 'share')
    gazebo_ros_dir = get_package_share_directory('gazebo_ros')
    # use_sim_time = LaunchConfiguration('use_sim_time') 
    model_arg = DeclareLaunchArgument(name='model', default_value=os.path.join(
                                        Model_Robot_description_dir, 'urdf', 'welding_robot.urdf'
                                        ),
                                      description='Absolute path to robot urdf file'
    )

    env_var = SetEnvironmentVariable('GAZEBO_MODEL_PATH', Model_Robot_description_share)

    # urdf_file_name = 'welding_robot.urdf'
    # urdf = os.path.join(
    #     get_package_share_directory('Model_Robot'),
    #     'urdf',
    #     urdf_file_name
    #     )
    # with open(urdf, 'r') as infp:
    #     robot_desc = infp.read()

    # robot_description = {"robot_description": robot_desc}


    start_gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_dir, 'launch', 'gzserver.launch.py')
        )
    )

    start_gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_dir, 'launch', 'gzclient.launch.py')
        )
    )

    spawn_robot = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-entity', 'welding_robot',
                                   '-topic', 'robot_description',
                                #    '-s', 'libgazebo_ros_control.so',
                                  ],
                        output='screen'
    )

    load_joint_state_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_state_broadcaster'],
        output='screen'
    )

    load_joint_trajectory_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'arm_controller'],
        output='screen'
    )

    # # Warehouse mongodb server
    # mongodb_server_node = Node(
    #     package="warehouse_ros_mongo",
    #     executable="mongo_wrapper_ros.py",
    #     parameters=[
    #         {"warehouse_port": 33829},
    #         {"warehouse_host": "localhost"},
    #         {"warehouse_plugin": "warehouse_ros_mongo::MongoDatabaseConnection"},
    #     ],
    #     output="screen",
    # )

    return LaunchDescription(
        [
        # RegisterEventHandler(
        #     event_handler=OnProcessExit(
        #         target_action=spawn_robot,
        #         on_exit=[load_joint_state_controller],
        #     )
        # ),
        # RegisterEventHandler(
        #     event_handler=OnProcessExit(
        #         target_action=load_joint_state_controller,
        #         on_exit=[load_joint_trajectory_controller],
        #     )
        # ),
            # ros2_control_node,
            joint_state_broadcaster_spawner,
            arm_controller_spawner,
            # tutorial_arg,
            # rviz_node_tutorial,


            rviz_node,
            static_tf,
            robot_state_publisher,
            run_move_group_node,  

            # control_node,          
            # # mongodb_server_node,

            #gazebo node
            env_var,
            model_arg,
            start_gazebo_server,
            start_gazebo_client,
            spawn_robot,

        ]
        # + load_controllers
    )