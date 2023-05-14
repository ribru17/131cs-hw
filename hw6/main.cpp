#include <cstddef>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using namespace std;

void foo(int x) {
    try {
        try {
            switch (x) {
            case 0:
                throw range_error("out of range error");
            case 1:
                throw invalid_argument("invalid_argument");
            case 2:
                throw logic_error("invalid_argument");
            case 3:
                throw bad_exception();
            case 4:
                break;
            }
        } catch (logic_error &le) {
            cout << "catch 1\n";
        }
        cout << "hurray!\n";
    } catch (runtime_error &re) {
        cout << "catch 2\n";
    }
    cout << "I'm done!\n";
}

void bar(int x) {
    try {
        foo(x);
        cout << "that's what I say\n";
    } catch (exception &e) {
        cout << "catch 3\n";
        return;
    }
    cout << "Really done!\n";
}

template <typename T> class Kontainer {
  private:
    T *min_el;
    T array[100];
    size_t size = 0;

  public:
    Kontainer() {
        min_el = nullptr;
    }

    void addVal(T val) {
        if (!min_el || val < *min_el) {
            min_el = &array[size];
        }
        array[size++] = val;
    }

    T getMin() {
        if (min_el) {
            return *min_el;
        } else {
            throw runtime_error("No values in Kontainer yet!");
        }
    }
};

int main() {
    Kontainer<string> *str_kont = new Kontainer<string>();
    str_kont->addVal("hi");
    str_kont->addVal("hiiii");
    str_kont->addVal("zUP");
    cout << str_kont->getMin() << endl; // prints "hi";

    Kontainer<double> *dub_kont = new Kontainer<double>();
    dub_kont->addVal(6.9);
    dub_kont->addVal(0.00023);
    dub_kont->addVal(10000000);
    cout << dub_kont->getMin() << endl; // prints 0.00023
}
