#!/bin/bash

mkdir -p build
rm -rf build/*
cd build
cmake .. -DCMAKE_VERBOSE_MAKEFILE=ON -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_BUILD_TYPE=Debug
make
