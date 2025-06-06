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
        char character;
    public:
        void move(vector<int> player_position, vector<int>& position){
            int xDistance = player_position.at(0) - position.at(0);
            int yDistance = player_position.at(1) - position.at(1);
            
            if(xDistance > 0){
                position.at(0)++;
            }else if(xDistance < 0){
                position.at(0)--;
            };

            if(yDistance > 0){
                position.at(1)++;
            }else if(yDistance < 0){
                position.at(1)--;
            };
        }

        Enemy():
            character('O')
        {

        }

        void addToScreen(vector<vector<char>>& screen, vector<int> position){
            screen.at(position.at(1)).at(position.at(0)) = character;
        }

};


class Player
{
    private:
        vector<int> position;
        int dashDistance;
        bool dash_toggle;
        vector<int> dashDirection;
        int dashDirectionInt;
        char character;

    public:

        Player(vector<int> pos):
            position(pos),
            dashDistance(2),
            dash_toggle(false),
            dashDirection({1,0}),
            dashDirectionInt(1),
            character('0')
        {

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

        int dash(vector<vector<char>> screen){
            if(!dash_toggle) {
                return 0;
            }

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

        void addToScreen(vector<vector<char>>& screen){
            screen.at(position.at(1)).at(position.at(0)) = character;
        }

        void toggleDashToggle(){
            if(dash_toggle){
                dash_toggle = false;
            }else{
                dash_toggle = true;
            }
        }

        vector<int> getPosition(){
            return position;
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


void addAndMoveAllEnemy(vector<vector<Enemy, int>> Enemies, vector<vector<char>>& screen, Player player){
    for(int i = 0; i < Enemies.size(); i++){
        Enemies.at(i).at(0).move(player.getPosition(), Enemies.at(i).at(1), Enemies.at(i).at(2));
        Enemies.at(i).at(0).addToScreen(screen, Enemies.at(i).at(1), Enemies.at(i).at(2));
    };
}


void newEnemy(vector<vector<Enemy, int>>& Enemies, int width, int height){
    Enemy enemy();
    Enemies.push_back({enemy, rand() % width, rand() % height});
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
    vector<vector<Enemy>> Enemies = {};
    int totalEnemies = 0;

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
                player.toggleDashToggle();
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
            default:
                player.dash(screen);
                break;
        };

        if(totalEnemies < 10){
            newEnemy(Enemies, width, height);
            totalEnemies++;
        };

        addAndMoveAllEnemy(Enemies, screen, player);
        player.addToScreen(screen);

        display(screen);
        Sleep(1);
    };
    

    return 0;
}
