cmake_minimum_required(VERSION 3.8)
project(serial_motor_msgs)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/EncoderVals.msg"
  "msg/MotorCommands.msg"
  "msg/MotorVels.msg"
  )
ament_export_dependencies(rosidl_default_runtime)
ament_package()

