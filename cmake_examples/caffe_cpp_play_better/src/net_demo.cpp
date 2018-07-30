#include <caffe/caffe.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <algorithm>
#include <iosfwd>
#include <memory>
#include <string>
#include <utility>
#include <vector>

// 需要先安装了opencv

using namespace caffe;  // NOLINT(build/namespaces)
using std::string;
using std::cout;
using std::endl;

/*
目的：
加载RCF网络
输入图片
网络前传
获取crop1的两个blob
手动调用auto_crop_layer
调用过程中进入caffe代码debug?
*/


int main(){
  Caffe::set_mode(Caffe::CPU);
  string prototxt = "test.prototxt";
  string caffemodel = "rcf_pretrained_bsds.caffemodel";
  
  shared_ptr<Net<float> > net;
  net.reset(new Net<float>(prototxt, TEST));
  net->CopyTrainedLayersFrom(caffemodel);

  CHECK_EQ(net->num_inputs(), 1) << "Network should have exactly one input.";
  CHECK_EQ(net->num_outputs(), 1) << "Network should have exactly one output.";

  cout << "在CPU模式下，建立了RCF网络" << endl;

  return 0;
}