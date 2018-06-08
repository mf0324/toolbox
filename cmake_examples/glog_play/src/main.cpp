#include <glog/logging.h>

int main(int argc, char* argv[]) {
    // Initialize Google's logging library.
    google::InitGoogleLogging(argv[0]);

    // ...
    FLAGS_log_dir = "./log";
    int num_cookies = 3;
    LOG(INFO) << "Found " << num_cookies << " cookies";
}
