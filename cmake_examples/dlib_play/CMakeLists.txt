cmake_minimum_required(VERSION 3.1)

# Define project name
project(dlib_play)

# C++11标准
set (CMAKE_CXX_STANDARD 11)

# 用于找到dlib编译好的各种lib和头文件
if (CMAKE_SYSTEM_NAME MATCHES "Windows")
    set( ENV{dlib_DIR} "D:/work/dlib/build/install/lib/cmake/dlib" )
    find_package(dlib REQUIRED)
elseif (CMAKE_SYSTEM_NAME MATCHES "Linux")
    set(dlib_INCLUDE_DIRS "/opt/work/dlib")   #dlib头文件路径，改成你的
    set(dlib_LIBS "/opt/work/dlib/build/dlib")  #dlib库文件路径，改成你的。使得包含dlib.lib文件

    # pthread库，在linux下必须。
    set(CMAKE_CXX_FLAGS -pthread)

endif (CMAKE_SYSTEM_NAME MATCHES "Windows")


# 添加头文件搜索路径
INCLUDE_DIRECTORIES(${dlib_INCLUDE_DIRS})

# 添加库文件搜索路径
link_directories(${dlib_LIBS})


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

# 添加可执行文件
my_add_executable(app src/face_detection_ex.cpp)

# add_library(app SHARED vl)

# 链接到库文件


if (CMAKE_SYSTEM_NAME MATCHES "Windows")
	target_link_libraries(app dlib::dlib)   # 这里很奇怪。window上必须要用dlib::dlib。linux下用dlib就可以。
elseif (CMAKE_SYSTEM_NAME MATCHES "Linux")
    target_link_libraries(app dlib)   # 这里很奇怪。window上必须要用dlib::dlib。linux下用dlib就可以。
endif (CMAKE_SYSTEM_NAME MATCHES "Windows")
