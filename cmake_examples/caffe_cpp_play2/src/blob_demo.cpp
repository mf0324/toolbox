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

    float* p = a.mutable_cpu_data();
    for(int i=0; i<a.count(); i++) {
        p[i] = i;
    }

    for(int u=0; u<a.num(); u++) {
        for(int v=0; v<a.channels(); v++) {
        }
    }

    return 0;
}
