#include <iostream>

class my_shared_ptr {
  private:
    int *ptr = nullptr;
    int *refCount = nullptr; // a)
  public:
    // b) constructor
    my_shared_ptr(int *ptr) {
        this->ptr = ptr;
        this->refCount = new int(1);
    } // c) copy constructor
    my_shared_ptr(const my_shared_ptr &other) {
        this->ptr = other.ptr;
        this->refCount = other.refCount;
        (*this->refCount)++;
    }
    // d) destructor
    ~my_shared_ptr() {
        if (--(*this->refCount) == 0) {
            delete this->refCount;
            delete this->ptr;
        }
    }
    // e) copy assignment
    my_shared_ptr &operator=(const my_shared_ptr &obj) {
        // don't do anything if we reassign to ourself
        if (&obj == this) {
            return *this;
        }
        // destruct the self
        this->~my_shared_ptr();

        // reinitialize self with the passed in obj, increment reference count
        this->ptr = obj.ptr;
        this->refCount = obj.refCount;
        (*this->refCount)++;
        return *this;
    }

    void showInfo() {
        std::cout << "val: " << *this->ptr << std::endl;
        std::cout << "ref count: " << *this->refCount << std::endl;
    }
};

int main() {
    auto ptr1 = new int(100);
    auto ptr2 = new int(200);
    my_shared_ptr m(ptr1); // should create a new shared_ptr for ptr1
    my_shared_ptr n(ptr2);
    my_shared_ptr o(n);
    n = m;
    // n = n;

    std::cout << "showing info: ";
    o.showInfo();
    o = m;
    std::cout << "info out" << std::endl;

    std::cout << "done" << std::endl;
    return 0;
}
