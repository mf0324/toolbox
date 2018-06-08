## For window users

**prerequesties**
cmake
visual studio 2015
opencv, build by 2015, by opencv official or self-compiled.


1. First, make sure `CMakeLists.txt` contains the correct opencv related path.

2. Do cmake build
```
compile.bat
```

3. Copy opencv dll to `build`
For example, I use opencv320. So I copy these:
```
opencv_world320.dll
opencv_world320d.dll
```

## For Linux users

**prerequesties**
cmake
opencv
g++

1. First, make sure `CMakeLists.txt` contains the correct opencv related path.

2. Do cmake build
```
mkdir build
cd build
cmake ..
```

3. make
