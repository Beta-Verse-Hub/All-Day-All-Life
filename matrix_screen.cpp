#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <string>
#include <conio.h>
#include <windows.h>

using namespace std;


vector<vector<char>> makeScreen(int& width, int& height){
    vector<vector<char>> screen;
    
    for(int y = 0; y < height; y++){
        screen.push_back(vector<char>());

        for(int x = 0; x < width-1; x++){
            screen.at(y).push_back(' ');
        };

    };

    return screen;
}


int display(vector<vector<char>> screen){

    string screenString = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n";
   
    for(int y = 0; y < screen.size(); y++){

        for(int x = 0; x < screen.at(y).size(); x++){
            screenString += screen.at(y).at(x);
        };

        if(y < screen.size()-1){
            screenString += "\n";
        }else{
            screenString.pop_back();
        };

    };

    cout << "\033[38;2;0;255;0m" << screenString << "\033[0m";

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
        };
        position = {rand() % width-1, -length};
    };

    bool move(int height) {
        position[1]++;
        return position[1] > height - 1;
    };

    vector<vector<char>> addToScreen(vector<vector<char>> win) {
        for (int i = 0; i < characters.size(); i++) {

            if(position[1] + i >= 0 && position[1]+i < win.size() && position[0] >= 0 && position[0] < win[0].size()-1){
                win[position[1]+i][position[0]] = characters[i];
            };
        };

        return win;
    };
};



int main(){
    
    system("");

    bool running = true;

    char key;
    vector<VerticalText> texts = {};

    while (running){
    
        
        int height, width;
        getTerminalSizeWindows(width, height);
        vector<vector<char>> screen = makeScreen(width, height);

        if (_kbhit()) {
            key = _getch();
        }else{
            key = '0';
        }

        int spawn_a_text = rand() % 6;

        if(spawn_a_text < 2){
            texts.push_back(VerticalText(width));
        };

        vector<int> atEnd = {};

        for(int i = 0; i < texts.size(); i++){
            VerticalText& text = texts.at(i);
            bool outOfBounds = text.move(height);
            screen = text.addToScreen(screen);
            if (outOfBounds)
            {
                atEnd.push_back(i);
            };
        };

        for(int i = atEnd.size()-1; i > 0; i--){
            texts.erase(texts.begin() + atEnd.at(i));
        };

        display(screen);

        if(key == 27){ // esc
            running = false;
        };

        Sleep(5);
    };

}