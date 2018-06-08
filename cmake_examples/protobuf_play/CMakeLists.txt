

cmake_minimum_required(VERSION 3.1)

# Define project name
project(protobuf_play)

# 使用c++11标准
set (CMAKE_CXX_STANDARD 11)

# 用来找到FindGFlags.cmake. 该文件来自Caffe源码. 需要先用apt安装gflags
#set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/Modules")
find_package(Protobuf REQUIRED)

if(protobuf_VERBOSE)
  message(STATUS "Using Protocol Buffers ${Protobuf_VERSION}")
endif()

message("PROTOBUF_INCLUDE_DIRS: ${PROTOBUF_INCLUDE_DIRS}")
message("PROTOBUF_LIBRARIES: ${PROTOBUF_LIBRARIES}")

# 添加可执行文件
add_executable(protobuf_play src/main.cpp src/proto/addressbook.pb.cc)

# 添加头文件搜索路径
INCLUDE_DIRECTORIES(
    src/proto  #为了找到*.pb.cc
    ./         #为了找到*.pb.h
)   

# Link your application with GLOG libraries
target_link_libraries(protobuf_play ${PROTOBUF_LIBRARIES})
