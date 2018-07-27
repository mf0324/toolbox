#include <stdio.h>

class Parent {
public:
    char data[20];
    void Function1();
    virtual void Function2();
};

void Parent::Function1(){
    printf("This is parent, function1\n");
}

void Parent::Function2(){
    printf("This is parent, function2\n");
}

class Child: public Parent{
    void Function1();
    void Function2();
};

void Child::Function1() {
    printf("This is child, function1\n");
}

void Child::Function2() {
    printf("This is child, function2\n");
}

int main(int argc, char** argv) {
    Parent parent;
    Child child;

    Parent* p;
    char t = getchar();
    if (t == 'c') {
        p = &child;
    } else{
        p = &parent;
    }
    p->Function1();
    p->Function2();

    return 0;
}
