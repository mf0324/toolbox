cmake_minimum_required(VERSION 3.1)

# Define project name
project(glags_play)

# 使用c++11标准
set (CMAKE_CXX_STANDARD 11)

# 用来找到FindGFlags.cmake. 该文件来自Caffe源码. 需要先用apt安装gflags
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/Modules")

find_package (GFlags REQUIRED)
#include_directories (${gflags_INCLUDE_DIR})

message("GFLAGS_INCLUDE_DIRS: ${GFLAGS_INCLUDE_DIRS}")
message("GFLAGS_LIBRARIES: ${GFLAGS_LIBRARIES}")

# 添加可执行文件
add_executable(gflags_play src/main.cpp)

# Link your application with gflags libraries
target_link_libraries(gflags_play ${GFLAGS_LIBRARIES})
