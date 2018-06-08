## 说明
本repo的代码为：用CMake构建的、最基本的protobuf工程(protobuf2,如果是protobuf3也类似)，测试环境为ubuntu，windows可能需要适当修改。
by imzhuo@foxmail.com

## 安装
```bash
sudo apt install cmake
sudo apt install libprotobuf-dev protobuf-compiler
```

## 编译：
```bash
rm src/proto/*.pb.*
protoc src/proto/addressbook.proto --cpp_out=./

mkdir -p build
rm -rf build/*
cd build
cmake ..
make
```

## 运行
```
./protobuf_play addressbook.data  #然后通过键盘输出多个字段，完成protobuf格式文件创建
```


