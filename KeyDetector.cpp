#include <conio.h>

using namespace std;

extern "C" __declspec(dllexport)

int get_key() {
    if(_kbhit()){
        return _getch();
    }
    return -1;
}
