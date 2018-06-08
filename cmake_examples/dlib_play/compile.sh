#!/bin/bash

mkdir -p build
rm -rf build/*
cd build

# must specify a same build type of existing dlib build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j3
