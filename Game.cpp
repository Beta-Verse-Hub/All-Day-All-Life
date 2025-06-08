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

        // Constructor
        Bullet(vector<int> player_position, int directionInt):
            position(player_position), // The position of the bullet is set to the position of the player.
            directionInt(directionInt), // The direction of the bullet as an int.
            direction([directionInt]() -> vector<int> { // The direction of the bullet as an vector.
                    switch(directionInt){
                        case  1: return { 0, 1};
                        case  2: return { 1, 0};
                        case -1: return { 0,-1};
                        case -2: return {-1, 0};
                        default: return { 0, 0};
                    };
                }()),
            character('+') // The character representing the bullet.
        {

        }

        //            ( 0,-1)
        //              -1
        //               |
        // (-1, 0) -2 ---+--- 2 ( 1, 0)
        //               |
        //               1
        //            ( 0, 1)

        // Moves the bullet in the current direction by updating its position.
        int move(vector<vector<char>>& screen, const int width, const int height){
            // Moves the bullet according to its direction.
            position.at(0) += direction.at(0);
            position.at(1) += direction.at(1);

            if(position.at(0) > width-2 || position.at(0) < 0 || position.at(1) > height-1 || position.at(1) < 0){
                return 2; // if the bullet has moved out of screen bounds.
            };
            if(screen.at(position.at(1)).at(position.at(0)) == 'O'){
                return 1; // if the bullet hits an enemy.
            }

            return 0; // if the bullet moves successfully without hitting anything.
        }

        // Returns the current position of the bullet.
        vector<int> getPosition() const{
            return position;
        }

        // Adds the character of the bullet to the screen at its current position.
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

        // Constructor
        Enemy(vector<int> pos):
            position(pos), // The position of the enemy.
            character('O'), // The character representing the enemy.
            speed(1) // The speed of the enemy.
        {

        }

        // Moves the enemy closer to the player's position according to the speed.
        void move(vector<int> player_position, const int width, const int height){
            int xDistance = player_position.at(0) - position.at(0);
            int yDistance = player_position.at(1) - position.at(1);
            
            // Does not move the enemy if it is already at the edge of the screen.
            if(xDistance > 0){
                position.at(0) += speed; // Moves the enemy to the right.
                if(position.at(0) > width-2){
                    position.at(0) = width-2; 
                }
            }else if(xDistance < 0){
                position.at(0) -= speed; // Moves the enemy to the left.
                if(position.at(0) < 0){
                    position.at(0) = 0;
                }
            };

            if(yDistance > 0){
                position.at(1) += speed; // Moves the enemy down.
                if(position.at(1) > height-1){
                    position.at(1) = height-1;
                }
            }else if(yDistance < 0){
                position.at(1) -= speed; // Moves the enemy up.
                if(position.at(1) < 0){
                    position.at(1) = 0;
                }
            };

        }

        // Returns the current position of the bullet.
        vector<int> getPosition() const{
            return position;
        }

        // Sets the position of the enemy to the given coordinates (x, y).
        void setPosition(int x, int y){
            position = {x, y};
        }

        // Adds the character of the enemy to the screen at its current position.
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
            position(pos), // The position of the player.
            dashDistance(3), // The distance the player dashes.
            dash_toggle(false), // The state of the dash.
            dashDirection({1,0}), // The direction of the dash.
            dashDirectionInt(1), // The direction of the dash as an integer.
            character('>') // The character representing the player.
        {

        }

        //            ( 0,-1)
        //              -1
        //               |
        // (-1, 0) -2 ---+--- 2 ( 1, 0)
        //               |
        //               1
        //            ( 0, 1)

        // Moves the player in the specified direction (x,y) and sets the player's character accordingly.
        void move(int x, int y, vector<vector<char>> screen){
            // Sets the direction of the dash.
            dashDirection = {x,y};
            dashDirectionInt = (2*x)+y;
            
            // Sets the character of the player.
            switch(dashDirectionInt){
                case -2:
                    character = '<'; // Left
                    break;
                case -1:
                    character = '^'; // Up
                    break;
                case 2:
                    character = '>'; // Right
                    break;
                case 1:
                    character = 'v'; // Down
                    break;
                default:
                    character = '~'; // Idle
                    break;
            }
        }

        // Dashes the player in the direction set by the dashDirection variable
        int dash(vector<vector<char>> screen){
            // Returns 1 if the player is not dashing.
            if(!dash_toggle) {
                return 1;
            }

            // Moves the player in the direction of the dash.
            position.at(0) += dashDistance*dashDirection.at(0);
            position.at(1) += dashDistance*dashDirection.at(1);
            
            if(position.at(0) < 0){ // If the player's x is less than screen width
                // Player's x will be set to screen width - 2
                position.at(0) = screen.at(0).size()-2;
            }else if(position.at(1) < 0){ // If the player's y is less than screen height
                // Player's y will be set to screen height - 1
                position.at(1) = screen.size()-1;
            }else if(position.at(0) > screen.at(0).size()-2){ // If the player's x is greater than screen width
                // Player's x will be set to 0
                position.at(0) = 0;
            }else if(position.at(1) > screen.size()-1){ // If the player's y is greater than screen height
                // Player's y will be set to 0
                position.at(1) = 0;
            };

            return 0;
        }

        // Adds the character of the player to the screen at its current position.
        void addToScreen(vector<vector<char>>& screen){
            screen.at(position.at(1)).at(position.at(0)) = character;
        }

        // Toggles the state of the dash.
        void toggleDashToggle(){
            if(dash_toggle){
                dash_toggle = false;
            }else{
                dash_toggle = true;
            }
        }

        // Returns the current position of the player.
        vector<int> getPosition() const{
            return position;
        }

        // Returns the direction of the dash as an integer.
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
    auto it = remove_if(Bullets.begin(), Bullets.end(), [&](Bullet& bullet){
        int hit_enemy = bullet.move(screen, width, height);
        if (hit_enemy == 1) {
            shotted_enemy = find_shotted_enemy(Enemies, bullet.getPosition());
            return true;
        } else if (hit_enemy == 2) {
            return true;
        }
        bullet.addToScreen(screen);
        return false;
    });
    
    // erase bullets
    Bullets.erase(it, Bullets.end());
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
        Sleep(20);
    };
    

    return 0;
}
