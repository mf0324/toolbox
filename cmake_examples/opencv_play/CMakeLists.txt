cmake_minimum_required(VERSION 3.1)

# Define project name
project(opencv_play)

# 至少使用c++0x标准
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x")
set (CMAKE_CXX_STANDARD 11)

# 用于找到opencv编译好的各种lib和头文件
if (CMAKE_SYSTEM_NAME MATCHES "Windows")
    list(APPEND CMAKE_PREFIX_PATH "D:/work/opencv320/build")
elseif (CMAKE_SYSTEM_NAME MATCHES "Linux")
    list(APPEND CMAKE_PREFIX_PATH "/home/chris/work/gitdown/opencv-2.4.13/build")
endif (CMAKE_SYSTEM_NAME MATCHES "Windows")
find_package(OpenCV REQUIRED)

# If the package has been found, several variables will
# be set, you can find the full list with descriptions
# in the OpenCVConfig.cmake file.
# Print some message showing some of them
message(STATUS "OpenCV library status:")
message(STATUS "    version: ${OpenCV_VERSION}")
message(STATUS "    libraries: ${OpenCV_LIBS}")
message(STATUS "    include path: ${OpenCV_INCLUDE_DIRS}")

#添加openmp编译参数
# find_package(OpenMP REQUIRED)
# if (OPENMP_FOUND)
# 	message("OPENMP FOUND")
# 	set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
# 	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
# 	set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
# endif()

# 添加头文件搜索路径
# INCLUDE_DIRECTORIES(./include)

# 用来在VisualStudio中正确显示目录结构
function(assign_source_group)
    foreach(_source IN ITEMS ${ARGN})
        if (IS_ABSOLUTE "${_source}")
            file(RELATIVE_PATH _source_rel "${CMAKE_CURRENT_SOURCE_DIR}" "${_source}")
        else()
            set(_source_rel "${_source}")
        endif()
        get_filename_component(_source_path "${_source_rel}" PATH)
        string(REPLACE "/" "\\" _source_path_msvc "${_source_path}")
        source_group("${_source_path_msvc}" FILES "${_source}")
    endforeach()
endfunction(assign_source_group)

# 用来在VisualStudio中正确显示目录结构
function(my_add_executable)
	if (CMAKE_SYSTEM_NAME MATCHES "Windows")
		foreach(_source IN ITEMS ${ARGN})
			assign_source_group(${_source})
		endforeach()
		#message("${ARGV}\n")
	endif ()
	add_executable(${ARGV})
endfunction(my_add_executable)

set( source_list
	${CLASSIFIER_SRCS}
	${UTIL_SRCS}
	${NPD_DETECTOR_SRCS}
	${NPD_SRCS}
)

# 添加可执行文件
my_add_executable(app src/main.cpp)

# Link your application with OpenCV libraries
target_link_libraries(app ${OpenCV_LIBS})