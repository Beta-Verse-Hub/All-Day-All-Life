#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <string>
#include <conio.h>
#include <windows.h>

using namespace std;


class Bullet
{
    private:
        vector<int> position;
        char character;
        vector<int> direction;
        int directionInt;
    public:

        Bullet(vector<int> player_position, int directionInt):
            position(player_position),
            directionInt(directionInt),
            direction([directionInt]() -> vector<int> {
                    switch(directionInt){
                        case  1: return { 0, 1};
                        case  2: return { 1, 0};
                        case -1: return { 0,-1};
                        case -2: return {-1, 0};
                        default: return { 0, 0};
                    };
                }()),
            character('+')
        {

        }

        //            ( 0,-1)
        //              -1
        //               |
        // (-1, 0) -2 ---+--- 2 ( 1, 0)
        //               |
        //               1
        //            ( 0, 1)

        int move(vector<vector<char>>& screen, const int width, const int height){
            position.at(0) += direction.at(0);
            position.at(1) += direction.at(1);

            if(position.at(0) > width-2){
                position.at(0) = width-2;
            }else if(position.at(0) < 0){
                position.at(0) = 0;
            }else if(position.at(1) > height-1){
                position.at(1) = height-1;
            }else if(position.at(1) < 0){
                position.at(1) = 0;
            };

            if(screen.at(position.at(1)).at(position.at(0)) == 'O'){
                return 1;
            }

            return 0;
        }

        vector<int> getPosition() const{
            return position;
        }

        void addToScreen(vector<vector<char>>& screen){
            screen.at(position.at(1)).at(position.at(0)) = character;
        }

};


class Enemy
{
    private:
        vector<int> position;
        char character;
        int speed;
    public:

        Enemy(vector<int> pos):
            position(pos),
            character('O'),
            speed(1)
        {

        }
    
        void move(vector<int> player_position, const int width, const int height){
            int xDistance = player_position.at(0) - position.at(0);
            int yDistance = player_position.at(1) - position.at(1);
            
            if(xDistance > 0){
                position.at(0) += speed;
                if(position.at(0) > width-2){
                    position.at(0) = width-2;
                }
            }else if(xDistance < 0){
                position.at(0) -= speed;
                if(position.at(0) < 0){
                    position.at(0) = 0;
                }
            };

            if(yDistance > 0){
                position.at(1) += speed;
                if(position.at(1) > height-1){
                    position.at(1) = height-1;
                }
            }else if(yDistance < 0){
                position.at(1) -= speed;
                if(position.at(1) < 0){
                    position.at(1) = 0;
                }
            };

        }

        vector<int> getPosition() const{
            return position;
        }

        void setPosition(int x, int y){
            position = {x, y};
        }

        void addToScreen(vector<vector<char>>& screen){
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
            dashDistance(3),
            dash_toggle(false),
            dashDirection({1,0}),
            dashDirectionInt(1),
            character('>')
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
                default:
                    character = '~';
                    break;
            }
        }

        int dash(vector<vector<char>> screen){
            if(!dash_toggle) {
                return 1;
            }

            position.at(0) += dashDistance*dashDirection.at(0);
            position.at(1) += dashDistance*dashDirection.at(1);
            
            if(position.at(0) < 0){
                position.at(0) = 0;
            }else if(position.at(1) < 0){
                position.at(1) = 0;
            }else if(position.at(0) > screen.at(0).size()-2){
                position.at(0) = screen.at(0).size()-2;
            }else if(position.at(1) > screen.size()-1){
                position.at(1) = screen.size()-1;
            };

            return 0;
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

        vector<int> getPosition() const{
            return position;
        }

        int getDashDirectionInt() const{
            return dashDirectionInt;
        }

};



vector<vector<char>> makeScreen(const int width, const int height){
    vector<vector<char>> screen;
    
    for(int y = 0; y < height; y++){
        screen.push_back(vector<char>());

        for(int x = 0; x < width-1; x++){
            screen.at(y).push_back(' ');
        };

    };

    return screen;
}


int find_shotted_enemy(vector<Enemy>& Enemies, vector<int> bulletPosition){
    for(int i = 0; i < Enemies.size(); i++){
        if(bulletPosition == Enemies.at(i).getPosition()){
            return i;
        }
    };
    return -1;
}

int addAndMoveAllBullets(vector<Bullet>& Bullets, vector<Enemy>& Enemies, vector<vector<char>>& screen, const Player player, const int width, const int height){
    int shotted_enemy = -1;
    for(int i = 0; i < Bullets.size(); i++){
        bool hit_enemy = Bullets.at(i).move(screen, width, height);
        Bullets.at(i).addToScreen(screen);
        if(hit_enemy){
            shotted_enemy = find_shotted_enemy(Enemies, Bullets.at(i).getPosition());
        }
    };
    return shotted_enemy;
}


void shoot(vector<Bullet>& Bullets, Player player, const int width, const int height){
    Bullet bullet(player.getPosition(), player.getDashDirectionInt());
    Bullets.push_back(bullet);
}


void addAndMoveAllEnemy(vector<Enemy>& Enemies, vector<vector<char>>& screen, const Player player, const int width, const int height){
    for(int i = 0; i < Enemies.size(); i++){
        Enemies.at(i).move(player.getPosition(), width, height);
        Enemies.at(i).addToScreen(screen);
    };
}


void newEnemy(vector<Enemy>& Enemies, const int width, const int height){
    Enemy enemy({rand() % width-1, rand() % height-1});
    Enemies.push_back(enemy);
}


void changeEnemy(vector<Enemy>& Enemies, int const enemyIndex, int const width, int const height){
    Enemies.at(enemyIndex).setPosition(rand() % width-1, rand() % height-1);
}


int display(vector<vector<char>>& screen){

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
    vector<Enemy> Enemies = {};
    int totalEnemies = 0;
    vector<Bullet> Bullets = {};

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
                shoot(Bullets, player, width, height);
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
            case '/': // '/' key
                player.toggleDashToggle();
                break;
            default:
                player.dash(screen);
                break;
        };

        if(totalEnemies < 10){
            newEnemy(Enemies, width, height);
            totalEnemies++;
        };

        addAndMoveAllEnemy(Enemies, screen, player, width, height);
        int shotted_enemy = addAndMoveAllBullets(Bullets, Enemies, screen, player, width, height);
        if(shotted_enemy != -1){
            changeEnemy(Enemies, shotted_enemy, width, height);
        };
        player.addToScreen(screen);

        display(screen);
        Sleep(10);
    };
    

    return 0;
}
