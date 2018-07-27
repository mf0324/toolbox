## 说明
本repo的代码为：用CMake构建的、使用Caffe的C++接口运行分类网络(inference)的例子，测试环境为ubuntu，windows可能需要适当修改。
by imzhuo@foxmail.com

## 依赖
能用cmake编译好caffe即可

## 编译：
运行`./compile.sh`或如下代码：
```bash
mkdir -p build
rm -rf build/*
cd build
cmake ..
make
```

## 推理
运行`./run.sh`或如下代码：
```bash
./build/im_cls \
    /opt/work/caffe-BVLC/models/bvlc_alexnet/deploy.prototxt \
    /opt/work/lesion/data/imagenet_models/bvlc_alexnet.caffemodel \
    /opt/work/caffe-BVLC/data/ilsvrc12/imagenet_mean.binaryproto \
    /opt/work/caffe-BVLC/data/ilsvrc12/synset_words.txt \
    /opt/work/caffe-BVLC/examples/images/cat.jpg
```

运行结果输出：
>---------- Prediction for /opt/work/caffe-BVLC/examples/images/cat.jpg ----------  
0.3094 - "n02124075 Egyptian cat"  
0.1761 - "n02123159 tiger cat"  
0.1221 - "n02123045 tabby, tabby cat"  
0.1132 - "n02119022 red fox, Vulpes vulpes"  
0.0421 - "n02085620 Chihuahua"  