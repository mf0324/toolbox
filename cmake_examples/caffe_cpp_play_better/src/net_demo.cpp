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
using namespace cv;

using std::string;
using std::vector;
using std::cout;
using std::endl;


/*
目的：
(ok) 加载RCF网络
(ok) 输入图片
(ok) 网络前传
获取crop1的两个blob
手动调用auto_crop_layer
调用过程中进入caffe代码debug?
*/


// 根据Feature层的名字获取其在网络中的Index
//! Note: Net的Blob是指，每个层的输出数据，即Feature Maps
// char *query_blob_name = "conv1";
unsigned int get_blob_index(boost::shared_ptr< Net<float> > & net, string query_blob_name)
{
    cout << "!! blob names are: " << endl;
    vector< string > const & blob_names = net->blob_names();
    for( unsigned int i = 0; i != blob_names.size(); ++i ) 
    { 
        cout << "=== " << blob_names[i] << endl;
        if( query_blob_name == blob_names[i] ) 
        { 
            return i;
        } 
    }
    LOG(FATAL) << "Unknown blob name: " << query_blob_name;
}


int main(){
  // ======================
  // step 1
  // ======================
  Caffe::set_mode(Caffe::CPU);
  // Caffe::set_mode(Caffe::GPU);
  // int gpu_id = 0;
  // Caffe::SetDevice(gpu_id);
  string prototxt = "test.prototxt";
  string caffemodel = "rcf_pretrained_bsds.caffemodel";
  
  shared_ptr< Net<float> > net(new caffe::Net<float>(prototxt, TEST));

  net->CopyTrainedLayersFrom(caffemodel);
  CHECK_EQ(net->num_inputs(), 1) << "!! Network should have exactly one input.";
  cout << "在CPU模式下，建立了RCF网络" << endl;

  // ======================
  // step 2
  // ======================
  string im_pth = "2018.jpg";
  Mat im = cv::imread(im_pth, -1);
  CHECK(!im.empty()) << "!! Unabl to decode image " << im_pth;
  cout << "Loaded image " << im_pth << endl;
  cvtColor(im, im, cv::COLOR_BGR2RGB);
  
  // ======================
  // step 3
  // ====================== 
  Blob<float>* input_layer = net->input_blobs()[0];
  int N = 1;
  int C = input_layer->channels();
  int H = im.rows;
  int W = im.cols;

  cv::Size input_geometry = cv::Size(input_layer->width(), input_layer->height());
  cout << "!! input_geometry.height=" << input_geometry.height << ", input_geometry.width=" << input_geometry.width << endl;

  cout << "!! C=" << C << ", H=" << H << ", W=" << W << endl;
  input_layer->Reshape(N, C, H, W);
  net->Reshape(); // Forward dimension change to all layers

  vector<Mat> input_channels;
  float* input_data = input_layer->mutable_cpu_data();
  for (int i=0; i<input_layer->channels(); i++){
    Mat channel(H, W, CV_32FC1, input_data);
    input_channels.push_back(channel);
    input_data += W * H;
  }

  // preprocess on input image
  Mat im_float;
  im.convertTo(im_float, CV_32FC3);

  Mat im_normalized;
  // cv::Scalar im_mean_scalar = Scalar(104.00698793,116.66876762,122.67891434);
  cv::Scalar im_mean_scalar = Scalar(122.67891434, 104.00698793,116.66876762);
  im_float -= im_mean_scalar;

  cv::split(im_float, input_channels);

  CHECK(reinterpret_cast<float*>(input_channels.at(0).data)
      == net->input_blobs()[0]->cpu_data())
      << "Input channels are not wrapping the input layer of the network.";
  

  cout << "\n=== Just before Network forward" << endl;
  net->Forward();
  cout << "\n=== Network Forward OK" << endl;

  // ======================
  // step 4
  // ====================== 
  /*
  fuse = net.blobs['sigmoid-fuse'].data[0][0,:,:]
  fuse = 255 * (1-fuse)
  cv2.imwrite(save_pth, fuse)
  */

  //! Note: 根据CaffeNet的deploy.prototxt文件，该Net共有15个Blob，从data一直到prob    
  string query_blob_name = "sigmoid-fuse"; /* data, conv1, pool1, norm1, fc6, prob, etc */
  unsigned int blob_id = get_blob_index(net, query_blob_name);

  boost::shared_ptr<Blob<float> > blob = net->blobs()[blob_id];
  unsigned int num_data = blob->count(); 
  const float *blob_ptr = (const float *) blob->cpu_data();

  cout << "\n=== Get network blob data OK" << endl;

  string save_pth = "2018_fuse.png";
  Mat netout_im(H, W, CV_32FC1, input_data);
  Mat one_im = Mat::ones(H, W, CV_32FC1);
  Mat save_im = one_im - netout_im;
  save_im = 255 * save_im;
  save_im.convertTo(save_im, CV_8UC1);

  cout << "\n=== I'm OK" << endl;

  cv::imwrite(save_pth, save_im);
  cout << "Save image OK" << endl;

  return 0;
}