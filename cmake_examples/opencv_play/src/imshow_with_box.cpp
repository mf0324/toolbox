#include <iostream>
#include <string>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

int main() {
	string im_name = "/home/zz/data/VOCdevkit/VOC2007/JPEGImages/000001.jpg";
	Mat im = imread(im_name);
    
    // draw boxes
    Point pt1, pt2;
    Scalar color;
    int thickness = 1;
    int linetype = 8;
        
    // -- dog
    pt1 = Point(48, 240);
    pt2 = Point(195, 371);
    color = Scalar(0, 0, 255);
    rectangle(im, pt1, pt2, color, thickness, linetype);

    // -- person
    pt1 = Point(8, 12);
    pt2 = Point(352, 498);
    color = Scalar(0, 255, 0);
    rectangle(im, pt1, pt2, color, thickness, linetype);

	string win_name = "voc000001.jpg";
	namedWindow(win_name);
	imshow(win_name, im);
	waitKey(0);
	destroyAllWindows();

	return 0;
}
