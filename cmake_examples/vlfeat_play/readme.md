这里做了两件事：1.用cmake编译vlfeat 2. 一个cmake构建的项目中使用vlfeat。具体做法见本文下面的内容，代码则在`https://github.com/zchrissirhcz/vlfeat`.


[TOC]
- environment statement
- Compile vlfeat with cmake
- Compile example project with cmake

## environment statement
- win10
- visual studio 2015 (to support cmake project)
- cmake (>3.10)
- vlfeat
- matlab

## compile vlfeat with cmake
```
cd d:/work/vlfeat
mkdir build
cd build
cmake -G "Visual Studio 14 Win64"
```

Then goto `d:/work/vlfeat/build`, open `vlfeat.sln`, choose `Release` as build type, and choose `ALL_BUILD` and `INSTALL`, run then repectively.

## compile example project with cmake

### 1. make sure custom settings
Goto the folder `d:/work/vlfeat/example/example-cmake-project` (or copy this folder to your working folder), check the paths in `CMakeLists.txt`. You should change the vlfeat's include and library directories to yours.

Also, copy `vl.dll` from `D:/work/vlfeat/build/Release` to `d:/work/vlfeat/example/example-cmake-projects`.

### 2. compile and run
Run `compile.bat`.

Note: you may see `compile.bat` and change it to linux scripts.

Then, goto its `build` folder and open `example-cmake-project.sln`. It will open Visual Studio.

Then run it.