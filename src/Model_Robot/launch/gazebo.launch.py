# import os
  
# from ament_index_python.packages import get_package_share_directory
 
# from launch_ros.parameter_descriptions import ParameterValue
# from launch.launch_description_sources import PythonLaunchDescriptionSource
# from launch import LaunchDescription
# from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
# from launch.conditions import IfCondition
# from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
# from launch_ros.actions import Node
# from launch_ros.substitutions import FindPackageShare
# from launch.actions import RegisterEventHandler
# from launch.event_handlers import OnProcessExit
  
# def generate_launch_description():
 
 
#     model_arg = DeclareLaunchArgument(name='model', description='Absolute path to robot urdf file')
#     pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
#     use_sim_time = LaunchConfiguration('use_sim_time') 
#     package_name = 'Model_Robot'
#     pkg_share = FindPackageShare(package=package_name).find(package_name)
#     pkg_gazebo_ros = FindPackageShare(package='gazebo_ros').find('gazebo_ros') 

#     #world_file_path = 'world.world'
#     #world = LaunchConfiguration('world')
#     #world_path = os.path.join(pkg_share, 'worlds',  world_file_path)

#     declare_use_sim_time_cmd = DeclareLaunchArgument(
#         name='use_sim_time',
#         default_value='true',
#         description='Use simulation (Gazebo) clock if true'
#         )

#     robot_name_in_model = 'welding_robot'

#     # Get URDF via xacro

#     urdf_file_name = 'welding_robot.urdf'
#     urdf = os.path.join(
#         get_package_share_directory('Model_Robot'),
#         'urdf',
#         urdf_file_name
#         )
#     with open(urdf, 'r') as infp:
#         robot_desc = infp.read()

#     robot_description = {"robot_description": robot_desc}
 
 
#     #rivz2
#     rviz2 = Node(
#         package='rviz2',
#         executable='rviz2',
#         name='rviz2',
#         output='log',
#         parameters=[{'use_sim_time': use_sim_time}],
#     )

#     tf_footprint_base = Node(
#         package='tf',
#         executable='static_transform_publisher',
#         arguments="0 0 0 0 0 0 base_link base_footprint 40",
#         name='tf_footprint_base',
#     )

#     fake_joint_calibration = Node(
#         package='rostopic',
#         executable='rostopic',
#         arguments="pub /calibrated std_msgs/Bool true",
#         name='fake_joint_calibration',
#     )
 
#     robot_state_publisher_node = Node(
#         package='robot_state_publisher',
#         executable='robot_state_publisher',
#         parameters= [{'use_sim_time': use_sim_time, 'robot_description': robot_desc}] #[{'use_sim_time': use_sim_time, "robot_description": robot_description_content}],
#     )

#     start_joint_state_publisher_cmd = Node(
#         package='joint_state_publisher',
#         executable='joint_state_publisher',
#         parameters=[{'use_sim_time': use_sim_time}],
#         name='joint_state_publisher',
#     )
 

#     '''declare_world_cmd = DeclareLaunchArgument(
#         name='world',
#         default_value=world_path,
#         description='Full path to the world model file to load'
#         ) '''
 
#     #spawn the robot 
#     spawn = Node(
#         package='gazebo_ros',
#         executable='spawn_entity.py',
#         arguments=["-topic", "/robot_description", 
#                     "-entity", robot_name_in_model,
#                     "-x", '0.0',
#                     "-y", '0.0',
#                     "-z", '0.0',
#                     "-Y", '0.0']
#     )


#     gazebo = ExecuteProcess(
#         cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so', 
#         '-s', 'libgazebo_ros_init.so'], output='screen',
#         )

     
#     return LaunchDescription([
#     declare_use_sim_time_cmd,
#     # tf_footprint_base,
#     spawn,
    
#     # fake_joint_calibration,
#     start_joint_state_publisher_cmd, 
#     robot_state_publisher_node,
#     gazebo,
# ])

import os
from ament_index_python.packages import get_package_share_directory, get_package_prefix

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.substitutions import Command, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    
    Model_Robot_description_dir = get_package_share_directory('Model_Robot')
    Model_Robot_description_share = os.path.join(get_package_prefix('Model_Robot'), 'share')
    gazebo_ros_dir = get_package_share_directory('gazebo_ros')
    # use_sim_time = LaunchConfiguration('use_sim_time') 
    model_arg = DeclareLaunchArgument(name='welding_robot', default_value=os.path.join(
                                        Model_Robot_description_dir, 'urdf', 'welding_robot.urdf'
                                        ),
                                      description='Absolute path to robot urdf file'
    )

    env_var = SetEnvironmentVariable('GAZEBO_MODEL_PATH', Model_Robot_description_share)

    urdf_file_name = 'welding_robot.urdf'
    urdf = os.path.join(
        get_package_share_directory('Model_Robot'),
        'urdf',
        urdf_file_name
        )
    with open(urdf, 'r') as infp:
        robot_desc = infp.read()

    robot_description = {"robot_description": robot_desc}

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters= [{'robot_description': robot_desc}] #[{'use_sim_time': use_sim_time, "robot_description": robot_description_content}],
    )


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

    return LaunchDescription([
        env_var,
        model_arg,
        start_gazebo_server,
        start_gazebo_client,
        robot_state_publisher_node,
        spawn_robot
    ])