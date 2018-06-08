#include <iostream>
#include <string>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

int main() {
	string im_name = "d:/work/toolbox/images/lena.jpg";
	Mat im = imread(im_name);

	string win_name = "lena";
	namedWindow(win_name);
	imshow(win_name, im);
	waitKey(0);
	destroyAllWindows();

	return 0;
}