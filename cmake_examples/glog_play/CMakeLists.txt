cmake_minimum_required(VERSION 3.1)

# Define project name
project(glog_play)

# 使用c++11标准
set (CMAKE_CXX_STANDARD 11)

# 用来找到FindGFlags.cmake. 该文件来自Caffe源码. 需要先用apt安装gflags
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/Modules")
find_package (Glog REQUIRED)

message("GLOG_INCLUDE_DIRS: ${GLOG_INCLUDE_DIRS}")
message("GLOG_LIBRARIES: ${GLOG_LIBRARIES}")

# 添加可执行文件
add_executable(glog_play src/main.cpp)

# Link your application with GLOG libraries
target_link_libraries(glog_play ${GLOG_LIBRARIES})
