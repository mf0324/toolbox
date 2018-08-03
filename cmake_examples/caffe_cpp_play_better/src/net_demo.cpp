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
#include <fstream>
#include <cassert>
#include <ctime>

// 需要先安装了opencv

using namespace caffe;  // NOLINT(build/namespaces)
using namespace cv;

using std::string;
using std::vector;
using std::cout;
using std::endl;
using std::ifstream;

/*
目的：
(ok) 加载RCF网络
(ok) 输入图片
(ok) 网络前传
(ok) 保存edgemap

把网络的forward()函数拆开来，自己写
获取crop1的两个blob
手动调用auto_crop_layer
调用过程中进入caffe代码debug?
*/


// 根据Feature层的名字获取其在网络中的Index
//! Note: Net的Blob是指，每个层的输出数据，即Feature Maps
// char *query_blob_name = "conv1";
unsigned int get_blob_index(boost::shared_ptr< Net<float> > & net, string query_blob_name){
	vector< string > const & blob_names = net->blob_names();
	for(size_t i = 0; i != blob_names.size(); ++i) {
		if( query_blob_name == blob_names[i] ){
			return i;
		}
	}
	LOG(FATAL) << "Unknown blob name: " << query_blob_name;
}

int main(int argc, char** argv){
    // ======================
    // step 1
    // ======================
    google::InitGoogleLogging("XXX");
    google::SetCommandLineOption("GLOG_minloglevel", "2");
    // Caffe::set_mode(Caffe::CPU);
    Caffe::set_mode(Caffe::GPU);
    int gpu_id = 7;
    Caffe::SetDevice(gpu_id);
    string prototxt = "test.prototxt";
    // string caffemodel = "rcf_pretrained_bsds.caffemodel";
    string caffemodel = "/home/zz/models/rcf_bdci_kongxinSmall_lrtune_iter_55000.caffemodel";

    shared_ptr< Net<float> > net(new caffe::Net<float>(prototxt, TEST));

    net->CopyTrainedLayersFrom(caffemodel);
    CHECK_EQ(net->num_inputs(), 1) << "!! Network should have exactly one input.";
    cout << "在CPU模式下，建立了RCF网络" << endl;

    // ======================
    // step 2
    // ======================
    // string im_pth = "2018.jpg";
    // string im_dir = "/home/zz/data/HED-BSDS/test";
    string im_dir = "/home/zz/data/BDCI_preliminary/JPEGImages";
    string im_lst_file = "test_im.lst";
    ifstream infile;
    infile.open(im_lst_file.data());
    assert(infile.is_open());
    string im_name, im_pth;
    while(getline(infile, im_name)) {
        clock_t start, finish;
        start = clock();
        im_pth = im_dir + "/" + im_name;
        Mat im = cv::imread(im_pth, -1);
        CHECK(!im.empty()) << "!! Unabl to decode image " << im_pth;
        cout << "processing " << im_pth;
        // cvtColor(im, im, cv::COLOR_BGR2RGB);

        // ======================
        // step 3
        // ======================
        Blob<float>* input_layer = net->input_blobs()[0];
        int N = 1;
        int C = input_layer->channels();
        int H = im.rows;
        int W = im.cols;

        cv::Size input_geometry = cv::Size(input_layer->width(), input_layer->height());

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

        cv::Scalar im_mean_scalar = Scalar(104.00698793,116.66876762,122.67891434);
        // cv::Scalar im_mean_scalar = Scalar(122.67891434, 104.00698793, 116.66876762);
        im_float -= im_mean_scalar;

        cv::split(im_float, input_channels);

        CHECK(reinterpret_cast<float*>(input_channels.at(0).data)
            == net->input_blobs()[0]->cpu_data())
            << "Input channels are not wrapping the input layer of the network.";

        finish = clock();
        double t_pre = (double)(finish - start) / CLOCKS_PER_SEC;
        cout << ", preprocess consume " << t_pre << " seconds";
        start = clock();
        //net->Forward();
        //==//net->ForwardFromTo(0, net->layers().size()-1);
        auto layers = net->layers();
        auto layer_names = net->layer_names();
        auto bottom_vecs = net->bottom_vecs();
        auto top_vecs = net->top_vecs();
        int num_layers = layers.size();
        for (int i=0; i<num_layers; i++) {
            layers[i]->Forward(bottom_vecs[i], top_vecs[i]);
        }
        finish = clock();
        double t_infer = (double)(finish - start) / CLOCKS_PER_SEC;
        cout << ", net inference consume " << t_infer << " seconds";
        cout << ", total " << t_pre + t_infer << " seconds\n";

        string query_blob_name = "sigmoid-fuse";
        unsigned int blob_id = get_blob_index(net, query_blob_name);

        boost::shared_ptr<Blob<float> > blob = net->blobs()[blob_id];
        const float *blob_ptr = blob->cpu_data();

        string save_pth = "fuse" + im_name;
        Mat netout_im(H, W, CV_32FC1, (float*)blob_ptr);
        Mat one_im = Mat::ones(H, W, CV_32FC1);
        Mat save_im = 255 * (one_im - netout_im);
        //save_im = 255 * save_im;
        save_im.convertTo(save_im, CV_8UC1);

        //cv::imwrite(save_pth, save_im);
        // cout << "\n=== Save image OK" << endl;
    }

    return 0;
}
