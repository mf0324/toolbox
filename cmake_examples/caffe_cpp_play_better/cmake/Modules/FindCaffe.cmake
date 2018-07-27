# Caffe package
unset(Caffe_FOUND)

### Set the variable Caffe_DIR as the root of our caffe directory
set(Caffe_DIR /opt/work/caffe-BVLC)
set(Caffe_Inst_DIR ${Caffe_DIR}/cmake_build/install)

find_path(Caffe_INCLUDE_DIRS NAMES caffe/caffe.hpp caffe/common.hpp caffe/net.hpp caffe/proto/caffe.pb.h caffe/util/io.hpp caffe/vision_layers.hpp
  HINTS
  ${Caffe_Inst_DIR}/include)



find_library(Caffe_LIBRARIES NAMES caffe
  HINTS
  ${Caffe_Inst_DIR}/lib)

message("Caffe_LIBRARIES HINTS is ${Caffe_DIR}/lib")
message("Caffe_LIBRARIES is ${Caffe_LIBRARIES}")

if(Caffe_LIBRARIES AND Caffe_INCLUDE_DIRS)
    set(Caffe_FOUND 1)
endif()
