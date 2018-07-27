cmake_minimum_required(VERSION 3.1)

# Define project name
project(caffe_cpp_play)

# 至少使用c++0x标准
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x")
set (CMAKE_CXX_STANDARD 11)


set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/Modules" )


set(PROJ_LINKER_LIBS "")
set(PROJ_INCLUDE_DIR "")

set(CMAKE_VERBOSE_MAKEFILE OFF)


##################################
#
# 设定option。根据option确定链接库
#
#################################
option(use_opencv "Use OpenCV?" ON)
option(use_cuda "Use CUDA?" ON)
option(use_glog "Use Glog?" ON)
option(use_gflags "Use GFlags?" ON)
option(use_protobuf "Use Protobuf?" ON)
option(use_caffe "Use Caffe?" ON)
option(use_boost "Use Boost?" ON)

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
if (use_opencv)
    #list(APPEND CMAKE_PREFIX_PATH "/opt/usr/opencv-git-3.4")
    #message("!!! CMAKE_PREFIX_PATH: ${CMAKE_PREFIX_PATH}")
    find_package(OpenCV REQUIRED)
    message(STATUS "OpenCV library status:")
    message(STATUS "    version: ${OpenCV_VERSION}")
    message(STATUS "    libraries: ${OpenCV_LIBS}")
    message(STATUS "    include path: ${OpenCV_INCLUDE_DIRS}")
    list(APPEND PROJ_LINKER_LIBS ${OpenCV_LIBS})
endif()


##################################
#
# CUDA
#
##################################
if (use_cuda)
    #list(APPEND CMAKE_PREFIX_PATH "/usr/local/cuda")
    set(CUDA_DIR "/usr/local/cuda")
    find_package(CUDA REQUIRED)
    include_directories(${CUDA_DIR}/include)
endif()


##################################
#
# Glog & GFlags & Protobuf
#
##################################
if (use_glog)
    find_package (Glog REQUIRED)         #OK
    list(APPEND PROJ_LINKER_LIBS ${GLOG_LIBRARIES})
endif()
if (use_gflags)
    find_package (GFlags REQUIRED)       #OK
    list(APPEND PROJ_LINKER_LIBS ${GFLAGS_LIBRARIES})
endif()
if (use_protobuf)
    find_package(Protobuf REQUIRED)      #OK
    list(APPEND PROJ_LINKER_LIBS ${PROTOBUF_LIBRARIES})
endif()


##################################
#
# Caffe
#
##################################
if (use_caffe)
    list(APPEND CMAKE_PREFIX_PATH "/home/zz/work/caffe-BVLC/build_cmake/install")
    find_package (Caffe REQUIRED)       #OK
    message(STATUS "Caffe library status:")
    message(STATUS "    Caffe_DIR: ${Caffe_DIR}")
    message(STATUS "    Caffe_LIBRARIES: ${Caffe_LIBRARIES}")
    message(STATUS "    CAFFE_INCLUDE_DIRS: ${Caffe_INCLUDE_DIRS}")
    list(APPEND PROJ_LINKER_LIBS ${Caffe_LIBRARIES})
endif()


##################################
#
# Boost
#
##################################
if (use_boost)
    find_package(Boost 1.54 REQUIRED COMPONENTS system thread filesystem regex)
    message(STATUS "Boost library status:")
    message(STATUS "    Boost_INCLUDE_DIRS: ${Boost_INCLUDE_DIRS}")
    message(STATUS "    Boost_LIBRARIES: ${Boost_LIBRARIES}")
    list(APPEND PROJ_LINKER_LIBS ${Boost_LIBRARIES})
endif()


# 添加头文件搜索路径
INCLUDE_DIRECTORIES(${Caffe_INCLUDE_DIRS})


# 添加可执行文件
#add_executable(im_cls src/im_cls.cpp)
add_executable(blob_demo src/blob_demo.cpp)

# Link your application with OpenCV libraries
# message("!!! PROJ_LINKER_LIBS: ${PROJ_LINKER_LIBS}")
#target_link_libraries(im_cls ${PROJ_LINKER_LIBS})
target_link_libraries(blob_demo ${PROJ_LINKER_LIBS})
