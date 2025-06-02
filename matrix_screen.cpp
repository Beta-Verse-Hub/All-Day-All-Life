#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <string>
#include <unistd.h>
#include <windows.h>

using namespace std;


vector<vector<char>> makeScreen(int& width, int& height){
    vector<vector<char>> screen;
    
    for(int y = 0; y < height; y++){
        screen.push_back(vector<char>());

        for(int x = 0; x < width; x++){
            screen.at(y).push_back(' ');
        };

    };

    return screen;
}


int display(vector<vector<char>> screen){

    string screenString = "";
   
    for(int y = 0; y < screen.size(); y++){

        for(int x = 0; x < screen.at(y).size(); x++){
            screenString += screen.at(y).at(x);
        };

        if(y < screen.size()-1){
            screenString += "\n";
        }else{
            screenString.pop_back();
        }

    };

    cout << screenString;

    return 0;
}


bool getTerminalSizeWindows(int& width, int& height) {
    CONSOLE_SCREEN_BUFFER_INFO csbi;
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);

    if (hConsole == INVALID_HANDLE_VALUE) {
        return false;
    }

    if (GetConsoleScreenBufferInfo(hConsole, &csbi)) {
        width = csbi.srWindow.Right - csbi.srWindow.Left + 1;
        height = csbi.srWindow.Bottom - csbi.srWindow.Top + 1;
        return true;
    }

    return false;
};


class VerticalText
{
private:
    int length;
    vector<char> characters;
    vector<int> position;
public:
    VerticalText(int width) {
        length = rand() % 14 + 7;
        for (int i = 0; i < length; ++i) {
            characters.push_back(static_cast<char>(rand() % (126 - 32 + 1) + 32));
        }
        position = {rand() % width, -length};
    }

    bool move(int height) {
        position[1]++;
        return position[1] > height - 1; // Return true if it goes out of bounds
    }
    void addToScreen(vector<vector<char>> win) {
        for (int i = 0; i < characters.size(); i++) {
            int a = win.size();
            if( a < position[1]+i ){
                win[position[1]+i][position[0]] = characters[i];
            }
        }
    }
};



int main(){
    int height, width;
    getTerminalSizeWindows(width, height);
    vector<vector<char>> screen = makeScreen(width, height);
    
    display(screen);

}