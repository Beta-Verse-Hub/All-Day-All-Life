#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <string>
#include <conio.h>
#include <windows.h>

using namespace std;


class Enemy
{
    private:
        vector<int> position;
        char character;
    public:
        void move(vector<int> player_position){
            int xDistance = player_position.at(0) - position.at(0);
            int yDistance = player_position.at(1) - position.at(1);
        }

        Enemy(vector<int> pos){
            position = pos;
            character = 'O';
        }

        vector<vector<char>> addToScreen(){
            
        }

};


class Player
{
    private:
        vector<int> position;
        int dashDistance;
        vector<int> dashDirection;
        int dashDirectionInt;
        char character;
    public:

        Player(vector<int> pos){
            vector<int> position = pos;
            int dashDistance = 5;
            vector<int> dashDirection = {1,0};
            int dashDirectionInt = 1;
            char character = '0';
        }

        //            ( 0,-1)
        //              -1
        //               |
        // (-1, 0) -2 ---+--- 2 ( 1, 0)
        //               |
        //               1
        //            ( 0, 1)

        void move(int x, int y, vector<vector<char>> screen){
            dashDirection = {x,y};
            dashDirectionInt = (2*x)+y;
            switch(dashDirectionInt){
                case -2:
                    character = '<';
                    break;
                case -1:
                    character = '^';
                    break;
                case 2:
                    character = '>';
                    break;
                case 1:
                    character = 'v';
                    break;
            }
        }

        void dash(vector<vector<char>> screen){
            position.at(0) += dashDistance*dashDirection.at(0);
            position.at(1) += dashDistance*dashDirection.at(1);
            
            if(position.at(0) < 0){
                position.at(0) = 0;
            }else if(position.at(1) < 0){
                position.at(1) = 0;
            }else if(position.at(0) > screen.at(0).size()-1){
                position.at(0) = screen.at(0).size()-1;
            }else if(position.at(1) > screen.size()-1){
                position.at(1) = screen.size()-1;
            };
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
    Player player({0,0});

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
            case 32: // Space key
                player.dash(screen);
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