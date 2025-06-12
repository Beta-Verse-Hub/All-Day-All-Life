#include <conio.h>

using namespace std;

extern "C" __declspec(dllexport)

int get_key() {
    return _getch();
}
