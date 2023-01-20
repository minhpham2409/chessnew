# define size of window
import pygame

#   --------------------    CONST   ------------------  #
import util
from GameState import GameState, Move

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = WIDTH / DIMENSION
MAX_FPS = 15
IMAGES = {}
icon = pygame.image.load('assets/images/icon.jpg')
colorBoard = [(255, 255, 255), (0, 102, 0), (255, 255, 0)]

WIDTH_PANEL = 300
HEIGHT_PANEL = 300

WIDTH_WINDOW = WIDTH + WIDTH_PANEL
HEIGHT_WINDOW = HEIGHT


#   --------------------    CONST   ------------------  #

# Load images into memory
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK',
              'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load(f"./assets/images/{piece}.png"), (SQ_SIZE, SQ_SIZE))


def main():
    pygame.init()
    loadImages()
    sound_move = pygame.mixer.Sound('./assets/sound/move.wav')
    sound_capture = pygame.mixer.Sound('./assets/sound/capture.wav')

    screen = pygame.display.set_mode((WIDTH_WINDOW, HEIGHT_WINDOW))
    board_screen = pygame.Surface((WIDTH, HEIGHT))
    panel_screen = pygame.Surface((WIDTH_PANEL, HEIGHT))

    pygame.display.set_caption("Cờ vua AI")
    pygame.display.set_icon(icon)

    gs = GameState()
    clock = pygame.time.Clock()

    click = ()  # Represent location of square which is pushed by mouse
    playerClicks = []
    moveMade = False
    validMoves = gs.getAllPossibleMoves()
    util.turn_print(gs.turn)
    running = True

    while running:
        #   Handle event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x = int(pos[1] / SQ_SIZE)
                y = int(pos[0] / SQ_SIZE)

                # Check valid screen
                if x in range(8) and y in range(8):
                    print(f'I click at ({x},{y}). It is {gs.board[x][y]}')

                    # case when first click is empty piece or another team
                    # or first click same as second click
                    if click == (x, y) or (not click and (gs.board[x][y] == '--' or gs.board[x][y][0] != gs.turn)):
                        print('Reset click')
                        click = ()
                        playerClicks = []
                    else:
                        click = (x, y)
                        playerClicks.append(click)
                    if len(playerClicks) == 2:
                        # Check click is in same team
                        if gs.board[playerClicks[0][0]][playerClicks[0][1]][0] == \
                                gs.board[playerClicks[1][0]][playerClicks[1][1]][0]:
                            print(" Check click is in same team")
                            click = playerClicks[1]
                            playerClicks = [click]
                        else:
                            move = Move(playerClicks[0], playerClicks[1], gs.board)
                            if move in validMoves:
                                if move.capturedPiece == '--':
                                    pygame.mixer.Sound.play(sound_move)
                                else:
                                    pygame.mixer.Sound.play(sound_capture)
                                gs.makeMove(move)
                                print(f'I have made a {move.getNotation()}')
                                moveMade = True
                            click = ()
                            playerClicks = []
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        gs.undoMove()
                        moveMade = True
                    if event.key == pygame.K_q:
                        util.logGameStatus(gs.capturedPieces)

        if moveMade:
            moveMade = False
            validMoves = gs.getAllPossibleMoves()
            util.turn_print(gs.turn)

        #   Update screen
        drawBoard(board_screen)
        drawPiece(board_screen, gs.board)
        highlightSquares(board_screen, gs.board, validMoves, click)

        drawPanel(panel_screen)

        screen.blit(board_screen, (0, 0))
        screen.blit(panel_screen, (WIDTH, 0))
        pygame.display.update()
        clock.tick(MAX_FPS)


def drawBoard(screen: pygame.Surface):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            color = colorBoard[(i + j) % 2]
            x = i * SQ_SIZE
            y = j * SQ_SIZE
            pygame.draw.rect(screen, color, pygame.Rect(x, y, SQ_SIZE, SQ_SIZE))


def drawPiece(broad_screen: pygame.Surface, board):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            piece = board[i][j]
            if piece != "--":
                broad_screen.blit(IMAGES[piece], pygame.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlightSquares(board_screen, board, validMoves, click):
    sqHighlight = []

    if click:
        for move in validMoves:
            if move.sqStart == click:
                sqHighlight.append(move.sqEnd)

        for (x, y) in sqHighlight:
            # pygame.draw.rect(screen, colorBoard[2], pygame.Rect(y*SQ_SIZE, x*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            surface = pygame.Surface((SQ_SIZE, SQ_SIZE))
            surface.set_alpha(150)
            surface.fill(colorBoard[2])
            board_screen.blit(surface, (y * SQ_SIZE, x * SQ_SIZE))


def drawPanel(panel_screen: pygame.Surface):
    panel_screen.fill(pygame.Color('white'))


if __name__ == "__main__":
    main()
