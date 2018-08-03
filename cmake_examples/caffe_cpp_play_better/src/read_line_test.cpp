#include <iostream>
#include <string>
#include <fstream>
#include <cassert>

using namespace std;

int main(){
	string file = "../test_im.lst";
    ifstream infile; 
    infile.open(file.data());   //将文件流对象与文件连接起来 
    assert(infile.is_open());   //若失败,则输出错误消息,并终止程序运行 

    string s;
	while(getline(infile,s)) {
        cout<<s<<endl;
    }
    infile.close();             //关闭文件输入流 

	return 0;
}
