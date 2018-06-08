cd build
del *

cmake -G "Visual Studio 14 Win64" ..
cmake --build . --config Release
cd ../