cmake_minimum_required(VERSION 3.1)

# Define project name
project(caffe_cpp_play)

# 至少使用c++0x标准
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x")
set (CMAKE_CXX_STANDARD 11)


set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/Modules" )


set(PROJ_LINKER_LIBS "")
set(PROJ_INCLUDE_DIR "")

##################################
#
# pThread
#
##################################
#find_package(Threads REQUIRED)
#message("CMAKE_THREAD_LIBS_INIT: ${CMAKE_THREAD_LIBS_INIT}")


##################################
#
# OpenCV
#
##################################
#list(APPEND CMAKE_PREFIX_PATH "/opt/usr/opencv-git-3.4")
message("!!! CMAKE_PREFIX_PATH: ${CMAKE_PREFIX_PATH}")
find_package(OpenCV REQUIRED)
message(STATUS "OpenCV library status:")
message(STATUS "    version: ${OpenCV_VERSION}")
message(STATUS "    libraries: ${OpenCV_LIBS}")
message(STATUS "    include path: ${OpenCV_INCLUDE_DIRS}")


##################################
#
# CUDA
#
##################################
#list(APPEND CMAKE_PREFIX_PATH "/usr/local/cuda")
set(CUDA_DIR "/usr/local/cuda")
#find_package(CUDA REQUIRED)
include_directories(${CUDA_DIR}/include)


##################################
#
# Glog & GFlags & Protobuf
#
##################################
find_package (GFlags REQUIRED)       #OK
find_package (Glog REQUIRED)         #OK
find_package(Protobuf REQUIRED)      #OK


##################################
#
# Caffe
#
##################################
list(APPEND CMAKE_PREFIX_PATH "/home/zz/work/caffe-BVLC/build/install")
find_package (Caffe REQUIRED)       #OK
message(STATUS "Caffe library status:")
message(STATUS "    Caffe_DIR: ${Caffe_DIR}")
message(STATUS "    Caffe_LIBRARIES: ${Caffe_LIBRARIES}")
message(STATUS "    CAFFE_INCLUDE_DIRS: ${Caffe_INCLUDE_DIRS}")


##################################
#
# Boost
#
##################################
find_package(Boost 1.54 REQUIRED COMPONENTS system thread filesystem regex)
message(STATUS "Boost library status:")
message(STATUS "    Boost_INCLUDE_DIRS: ${Boost_INCLUDE_DIRS}")
message(STATUS "    Boost_LIBRARIES: ${Boost_LIBRARIES}")


# 添加头文件搜索路径
INCLUDE_DIRECTORIES(${Caffe_INCLUDE_DIRS})


# 添加可执行文件
add_executable(im_cls src/im_cls.cpp)

# Link your application with OpenCV libraries
target_link_libraries(im_cls ${OpenCV_LIBS} ${Caffe_LIBRARIES} ${GLOG_LIBRARIES} ${GFLAGS_LIBRARIES} ${PROTOBUF_LIBRARIES} ${Boost_LIBRARIES})
