
//The purpose of this project is to teach someone new how to write a tic tac toe AI.

#include <iostream>
#include <string>

using namespace std;

void printBoard(string[3][3]);
int getPlayerRow(string);
int getPlayerColumn(string);
bool checkVictory(string[3][3], const string&);
bool checkEmptyBoard(string[3][3]);
string getAIMove(string[3][3]);
long calcMove(string[3][3], const string &, const string &);
int main(){

    string gameBoard[3][3] =  {{" ", " ", " "},
                                   {" ", " ", " "},
                                   {" ", " ", " "}};

    string playerMove;
    int inputRow;
    int inputColumn;
    string currentMove = "X";
    bool invalidMove = false;
    string aiMove = "O";

    printBoard(gameBoard);

        while(true){
        if(currentMove != aiMove){
        cout << "\n\nEnter Move: ";
        cin >> playerMove;
        } else
            playerMove = getAIMove(gameBoard);
            
        inputRow = getPlayerRow(playerMove);
        inputColumn = getPlayerColumn(playerMove);

        if(inputColumn == -1 || inputRow == -1 || gameBoard[inputRow][inputColumn] != " ")
            invalidMove = true;
        
        if(!invalidMove)
            gameBoard[inputRow][inputColumn] = currentMove;

        printBoard(gameBoard);

        if (checkVictory(gameBoard, currentMove)){
            cout << "\n\n"
                 << currentMove << " wins!";
            return 0;
        }

        if (checkEmptyBoard(gameBoard)){
            cout << "\n\nDraw!";
            return 0;
        }

        if(!invalidMove){
            if(currentMove == "X")
                currentMove = "O";
            else
                currentMove = "X";
        } else
            invalidMove = false;
    }

}


void printBoard(string board[3][3]){
    cout << endl << endl;
    cout << " " << board[0][0] << " | " << board[0][1] << " | " << board[0][2] << endl;
    cout << "-----------" << endl;
    cout << " " << board[1][0] << " | " << board[1][1] << " | " << board[1][2] << endl;
    cout << "-----------" << endl;
    cout << " " << board[2][0] << " | " << board[2][1] << " | " << board[2][2] << endl;
}

int getPlayerRow(string playerMove){
    if(playerMove[0] == 't' || playerMove[0] == '0')
        return 0;
    if(playerMove[0] == 'm' || playerMove[0] == '1')
        return 1;
    if(playerMove[0] == 'b' || playerMove[0] == '2')
        return 2;

    return -1;
}

int getPlayerColumn(string playerMove){
    if(playerMove[1] == 'l' || playerMove[1] == '0')
        return 0;
    if(playerMove[1] == 'c' || playerMove[1] == '1')
        return 1;
    if(playerMove[1] == 'r' || playerMove[1] == '2')
        return 2;

    return -1;
}

bool checkVictory(string board [3][3], const string& move){

    for (int i = 0; i < 3; i++){
        if(board[i][0] == board[i][1] && board[i][1] == board[i][2] && board[i][1] == move)
            return true;
        if(board[0][i] == board[1][i] && board[1][i] == board[2][i] && board[1][i] == move)
            return true;
    }

    if(board[0][0] == board[1][1] && board[1][1] == board[2][2] && board[1][1] == move ||
        board[2][0] == board[1][1] && board[1][1] == board[0][2] && board[1][1] == move)
        return true;

    return false;
}

bool checkEmptyBoard(string board[3][3]){
    for (int i = 0; i < 3; i++){
        for (int j = 0; j < 3; j++){
            if(board[i][j] == " ")
                return false;
        }
    }
    return true;
}

string getAIMove(string board[3][3]){
    int row = 5;
    int column = 5;
    long bestvalue = -1000;
    long value;

    for (int i = 0; i < 3; i++){
        for (int j = 0; j < 3; j++){
            if(board[i][j] == " "){
                board[i][j] = "O";

                if(checkVictory(board, "O"))
                    return to_string(i) + to_string(j);

                value = calcMove(board, "X", "O");
            }
        }
    }
}

long calcMove(string board[3][3], const string& nextMove, const string& lastMove){
    int value = 0;

    for (int i = 0; i < 3; i++){
        for (int j = 0; j < 3; j++){
            if(board[i][j] == " "){
                if(nextMove == "X")
                    return -1000;
                else
                    return 1000;
            
            value += calcMove(board, lastMove, nextMove);

            board[i][j] = " ";
            }
        }
    }
    return value / 10;
}