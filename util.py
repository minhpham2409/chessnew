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