def move_print(moves):
    for i in range(len(moves)):
        print(moves[i].getNotation(), sep=",")


def turn_print(turn):
    if turn == 'w':
        print("Turn belongs to white")
    else:
        print("Turn belongs to black")


def getNumberOfMoves(moves):
    print(f'It has total {len(moves)} possible moves')


def logGameStatus(capturedPieces):

    print("Display game status:")
    print("-------------------------White-------------------------")
    print(f"Capture Pawn: {capturedPieces['bp']}")

    print("-------------------------Black-------------------------")
    print(f"Capture Pawn: {capturedPieces['wp']}")


def printBoard(board):
    print('[',end='')
    for i in range(8):
        str = ','.join(board[i])
        print('[',end='')
        print(str,end='],')
        print('')
    print(']')


def printPinAndCheck(pins,checks):
    if len(checks)== 0:
        print("No checker")
    if len(pins) == 0:
        print("No pinner")

    print("Print checks: ")
    for i in range(len(checks)):
        print("Tọa độ: ", checks[i][0][0],checks[i][0][1], "Hướng: ",checks[i][1][0], checks[i][1][1],sep=", ",end="\n")

    print("Print pins: ")
    for i in range(len(pins)):
        print("Điểm pin: ", pins[i][0][0], pins[i][0][1], "Điểm check: ", pins[i][1][0], pins[i][0][1], sep=", ", end="\n")



