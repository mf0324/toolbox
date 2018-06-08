## 说明
本repo的代码为：用CMake构建的、最基本的gflags工程，测试环境为ubuntu，windows可能需要适当修改。
by imzhuo@foxmail.com

## 安装
```bash
sudo apt install cmake
sudo apt install libgflags-dev
```

## 编译：
```bash
mkdir -p build
cd build
cmake ..
make
```

## 运行
```
./gflags_play -verbose=0
./gflag_play -message=what
./gflags_play -message=like\?it   #问号需要用\转义
```