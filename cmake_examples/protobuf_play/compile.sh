#!/bin/bash

rm src/proto/*.pb.*
protoc src/proto/addressbook.proto --cpp_out=./

mkdir -p build
rm -rf build/*
cd build
cmake ..
make
