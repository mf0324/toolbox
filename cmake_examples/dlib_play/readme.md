# Readme

Though dlib provides example programs with a CMakeLists.txt script, however, it is not very easy to use that.

Instead, I think a very very tiny hello world cmake script is needed, and it should be run either on windows or ubuntu.

Part of this is inspired from `https://www.learnopencv.com/install-dlib-on-windows/`, but this script is easier that: you don't have to create envirionment in "control panel"->"user enviroment variables". Instead, it is created in the cmakelists.txt

## Steps on windows

### compile and install dlib with cmake
run this script `compile-dlib-windows.bat` under dlib root folder:
```
mkdir build
cd build
 
::This is a single command. Backticks are used for line continuation
cmake -G "Visual Studio 14 2015 Win64" ^
-DJPEG_INCLUDE_DIR=..\dlib\external\libjpeg ^
-DJPEG_LIBRARY=..\dlib\external\libjpeg ^
-DPNG_PNG_INCLUDE_DIR=..\dlib\external\libpng ^
-DPNG_LIBRARY_RELEASE=..\dlib\external\libpng ^
-DZLIB_INCLUDE_DIR=..\dlib\external\zlib ^
-DZLIB_LIBRARY_RELEASE=..\dlib\external\zlib ^
-DCMAKE_INSTALL_PREFIX=install ..
 
cmake --build . --config Release --target INSTALL
cd ..
```

### build this project with cmake
first make sure the `dlib_DIR` in `CMakeLists.txt` is correct under your computer.
Then makre sure visual studio 2015 is installed.

Then run `compile.bat`.

## Steps on linux
first build dlib with cmake as official said.
Then simply run `compile.sh`.