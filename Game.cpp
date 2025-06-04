#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <string>
#include <conio.h>
#include <windows.h>

using namespace std;


class Player
{
    private:
        vector<int> position = {0,0};
        int dashDistance = 5;
        char character = '0';
    public:
        void move(int x, int y, vector<vector<char>> screen){
            if(position.at(0) == 0 and x == -1){
                return;
            }else if(position.at(1) == 0 and y == -1){
                return;
            }else if(position.at(0) == screen.at(0).size()-1 and x == 1){
                return;
            }else if(position.at(1) == screen.size()-1 and y == 1){
                return;
            }
            position = {position.at(0) + x, position.at(1) + y};
        }

        void dash(){

        }

        vector<vector<char>> addToScreen(vector<vector<char>> screen){
            screen.at(position.at(1)).at(position.at(0)) = character;
            return screen;
        }
};


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
}


int main(){
    vector<vector<char>> screen;
    bool running = true;
    int width, height;
    char key;
    Player player = Player();

    while (running)
    {
        getTerminalSizeWindows(width, height);
        screen = makeScreen(width, height);

        if (_kbhit()) {
            key = _getch();
        }else{
            key = '0';
        };

        switch(key){
            case 27: // ESC key
                running = false;
                break;
            case 72: // up arrow
                player.move( 0,-1,screen);
                break;
            case 80: // down arrow
                player.move( 0, 1,screen);
                break;
            case 75: // left arrow
                player.move(-1, 0,screen);
                break;
            case 77: // right arrow
                player.move( 1, 0,screen);
                break;
        };

        screen = player.addToScreen(screen);
        display(screen);
        Sleep(1);
    };
    

    return 0;
}