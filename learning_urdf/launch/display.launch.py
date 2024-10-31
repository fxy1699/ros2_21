from ament_index_python.packages import get_package_share_path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    # 获取名为learning_urdf的ROS2包的共享路径。
    urdf_tutorial_path = get_package_share_path('learning_urdf')
    # 定义默认的URDF模型文件路径。
    default_model_path = urdf_tutorial_path / 'urdf/mbot_base.urdf'
    # 定义默认的RViz配置文件路径。
    default_rviz_config_path = urdf_tutorial_path / 'rviz/urdf.rviz'
    # 声明一个启动参数gui，用于控制是否启动joint_state_publisher_gui
    gui_arg = DeclareLaunchArgument(name='gui', default_value='false', choices=['true', 'false'],
                                    description='Flag to enable joint_state_publisher_gui')
    # 声明一个启动参数model，用于指定机器人的URDF文件路径
    model_arg = DeclareLaunchArgument(name='model', default_value=str(default_model_path),
                                      description='Absolute path to robot urdf file')
    # 声明一个启动参数rvizconfig，用于指定RViz的配置文件路径
    rviz_arg = DeclareLaunchArgument(name='rvizconfig', default_value=str(default_rviz_config_path),
                                     description='Absolute path to rviz config file')
    # 创建一个参数值，用于将URDF模型文件通过xacro命令转换，并传递给robot_state_publisher节点
    robot_description = ParameterValue(Command(['xacro ', LaunchConfiguration('model')]),
                                       value_type=str)
    # 创建一个节点，用于发布机器人的状态
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    # Depending on gui parameter, either launch joint_state_publisher or joint_state_publisher_gui
    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        condition=UnlessCondition(LaunchConfiguration('gui'))
    )
    # 创建一个节点，用于发布关节状态的GUI版本，但仅当gui参数为true时启动
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        condition=IfCondition(LaunchConfiguration('gui'))
    )
    # 创建一个节点，用于启动RViz，并加载指定的配置文件
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
    )
    # 返回一个LaunchDescription对象，其中包含了所有的启动参数和节点
    return LaunchDescription([
        gui_arg,
        model_arg,
        rviz_arg,
        joint_state_publisher_node,
        joint_state_publisher_gui_node,
        robot_state_publisher_node,
        rviz_node
    ])
