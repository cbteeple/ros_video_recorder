cmake_minimum_required(VERSION 2.8.3)
project(video_recorder)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
  rospy_message_converter
)

add_service_files(
  FILES
  RecordVideo.srv
  StopRecording.srv
)

generate_messages(
  DEPENDENCIES
  std_msgs  # Or other packages containing msgs
)

catkin_package(
  CATKIN_DEPENDS message_runtime
)

include_directories(
)
