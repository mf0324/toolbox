#!/bin/bash

mkdir -p build
rm -rf build/*
cd build
cmake .. -DCMAKE_VERBOSE_MAKEFILE=ON
make
