cmake_minimum_required(VERSION 3.1)

# Define project name
project(oh-my-traffic-sign)

# C++11标准
set (CMAKE_CXX_STANDARD 11)

# 添加头文件搜索路径
INCLUDE_DIRECTORIES(./include)
INCLUDE_DIRECTORIES("D:/work/vlfeat")

# 添加库文件搜索路径
LINK_DIRECTORIES("D:/work/vlfeat/build/Release")

# 用于找到vlfeat编译好的各种lib和头文件
if (CMAKE_SYSTEM_NAME MATCHES "Windows")
    # list(APPEND CMAKE_PREFIX_PATH "D:/lib/vlfeat/bin/win64")
	list(APPEND "D:/work/vlfeat/build/Release")
elseif (CMAKE_SYSTEM_NAME MATCHES "Linux")
    list(APPEND CMAKE_PREFIX_PATH "/home/chris/work/gitdown/opencv-2.4.13/build")
endif (CMAKE_SYSTEM_NAME MATCHES "Windows")


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

function(my_add_executable)
	if (CMAKE_SYSTEM_NAME MATCHES "Windows")
		foreach(_source IN ITEMS ${ARGN})
			assign_source_group(${_source})
		endforeach()
		#message("${ARGV}\n")
	endif ()
	add_executable(${ARGV})
endfunction(my_add_executable)

#add_library(
#"D:/work/vlfeat/vl/host.c"
#"D:/work/vlfeat/vl/random.c"
#"D:/work/vlfeat/vl/generic.c"
#"D:/work/vlfeat/vl/slic.c")

# 添加可执行文件
my_add_executable(app src/main.cpp)

# add_library(app SHARED vl)

# 链接到库文件
target_link_libraries(app vl)
