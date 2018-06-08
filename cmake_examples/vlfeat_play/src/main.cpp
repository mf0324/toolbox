extern "C" {
#include "vl/generic.h"
}

int main(int argc, const char * argv[]) {
	VL_PRINT("Hello, welcome to my first vlfeat c++ demo!");

	VlHog * hog = vl_hog_new(VlHogVariantDalalTriggs, numOrientations, VL_FALSE) ;
	vl_hog_put_image(hog, image, height, width, numChannels, cellSize) ;
	hogWidth = vl_hog_get_width(hog) ;
	hogHeight = vl_hog_get_height(hog) ;
	hogDimenison = vl_hog_get_dimension(hog) ;
	hogArray = vl_malloc(hogWidth*hogHeight*hogDimension*sizeof(float)) ;
	vl_hog_extract(hog, hogArray) ;
	vl_hog_delete(hog) ;

	glyphSize = vl_hog_get_glyph_size(hog) ;
	imageHeight = glyphSize * hogArrayHeight ;
	imageWidth = glyphSize * hogArrayWidth ;
	image = vl_malloc(sizeof(float)*imageWidth*imageHeight) ;
	vl_hog_render(hog, image, hogArray) ;

	return 0;
}