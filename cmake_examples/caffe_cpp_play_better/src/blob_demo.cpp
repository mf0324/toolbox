#include <iostream>
#include <vector>
#include <caffe/blob.hpp>

using namespace std;
using namespace caffe;

int main(){
    Blob<float> a;
    cout << "size:" << a.shape_string() << endl;
    a.Reshape(1, 2, 3, 4);
    cout << "size:" << a.shape_string() << endl;

    for(int i=0; i<a.num_axes(); i++){
        cout << "a.shape(" << i << ") = " << a.shape(i) << endl;
    }

    /*
    float* p = a.mutable_cpu_data();
    for(int i=0; i<a.count(); i++) {
        p[i] = i;
    }

    for(int u=0; u<a.shape(0); u++) {
        for(int v=0; v<a.channels(); v++) {
            for()
        }
    }
    */

    return 0;
}
