import sys
import pygame

#   --------------------    CONST   ------------------  #
import util
from GameState import GameState, Move

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = WIDTH / DIMENSION
MAX_FPS = 15
icon = pygame.image.load('assets/images/icon.jpg')
colorBoard = [(255, 255, 255), (0, 102, 0), (255, 255, 0)]

WIDTH_PANEL = 300
HEIGHT_PANEL = 300

WIDTH_WINDOW = WIDTH + WIDTH_PANEL
HEIGHT_WINDOW = HEIGHT


#   --------------------    CONST   ------------------  #


class GameMain:
    def __init__(self):
        self.IMAGES = {}

        pygame.init()
        self._loadImages()
        self._loadSound()

        # Surface for entire screen
        self.screen = pygame.display.set_mode((WIDTH_WINDOW, HEIGHT_WINDOW))
        # Surface for board game
        self.board_screen = pygame.Surface((WIDTH, HEIGHT))
        # Surface for game status and controller
        self.panel_screen = pygame.Surface((WIDTH_PANEL, HEIGHT))

        pygame.display.set_caption("Cờ vua AI")
        pygame.display.set_icon(icon)

        self.gs = GameState()
        self.clock = pygame.time.Clock()

        self.click = ()  # Represent location of square which is pushed by mouse
        self.playerClicks = []
        self.moveMade = False
        self.validMoves = self.gs.getAllPossibleMoves()
        util.turn_print(self.gs.turn)
        self.running = True

    def mainLoop(self):
        while self.running:
            #   Handle event
            self._eventHandler()

            #  move update
            if self.moveMade:
                self.moveMade = False
                self.validMoves = self.gs.getAllPossibleMoves()
                util.turn_print(self.gs.turn)

            #   Update screen
            self._drawScreen()
            pygame.display.update()
            self.clock.tick(MAX_FPS)

    # Load images into memory
    def _loadImages(self):
        pieces = ['wp', 'wR', 'wN', 'wB', 'wK',
                  'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
        for piece in pieces:
            self.IMAGES[piece] = pygame.transform.scale(pygame.image.load(f"./assets/images/{piece}.png"),
                                                        (SQ_SIZE, SQ_SIZE))

    # Load sound into memory
    def _loadSound(self):
        self.sound_move = pygame.mixer.Sound('./assets/sound/move.wav')
        self.sound_capture = pygame.mixer.Sound('./assets/sound/capture.wav')

    def _drawScreen(self):
        self._drawBoard()
        self._drawPiece()
        self._highlightSquares()
        self._drawPanel()
        self.screen.blit(self.board_screen, (0, 0))
        self.screen.blit(self.panel_screen, (WIDTH, 0))

    def _drawBoard(self):
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                color = colorBoard[(i + j) % 2]
                x = i * SQ_SIZE
                y = j * SQ_SIZE
                pygame.draw.rect(self.board_screen, color, pygame.Rect(x, y, SQ_SIZE, SQ_SIZE))

    def _drawPiece(self):
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                piece = self.gs.board[i][j]
                if piece != "--":
                    self.board_screen.blit(self.IMAGES[piece], pygame.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    def _highlightSquares(self):
        sqHighlight = []

        if self.click:
            for move in self.validMoves:
                if move.sqStart == self.click:
                    sqHighlight.append(move.sqEnd)

            for (x, y) in sqHighlight:
                # pygame.draw.rect(screen, colorBoard[2], pygame.Rect(y*SQ_SIZE, x*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                surface = pygame.Surface((SQ_SIZE, SQ_SIZE))
                surface.set_alpha(150)
                surface.fill(colorBoard[2])
                self.board_screen.blit(surface, (y * SQ_SIZE, x * SQ_SIZE))

    def _drawPanel(self):
        self.panel_screen.fill(pygame.Color('white'))

    def _eventHandler(self):
        for event in pygame.event.get():
            # Event occurs when click X button
            if event.type == pygame.QUIT:
                running = False
                sys.exit(1)
            # Event occurs when click into screen
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._clickHandler()
            # Event occurs when press into a key
            elif event.type == pygame.KEYDOWN:

                # Press z to undo
                if event.key == pygame.K_z:
                    self.gs.undoMove()
                    self.moveMade = True

                # Press q to log game_status
                if event.key == pygame.K_q:
                    util.logGameStatus(self.gs.capturedPieces)

    def _clickHandler(self):
        pos = pygame.mouse.get_pos()
        x = int(pos[1] / SQ_SIZE)
        y = int(pos[0] / SQ_SIZE)

        # Check valid screen
        if x in range(8) and y in range(8):
            print(f'I click at ({x},{y}). It is {self.gs.board[x][y]}')

            # case when first click is empty piece or another team
            # or first click same as second click
            if self.click == (x, y) or (not self.click and (
                    self.gs.board[x][y] == '--' or self.gs.board[x][y][0] != self.gs.turn)):
                print('Reset click')
                self.click = ()
                self.playerClicks = []
            else:
                self.click = (x, y)
                self.playerClicks.append(self.click)
            if len(self.playerClicks) == 2:
                # Check click is in same team
                if self.gs.board[self.playerClicks[0][0]][self.playerClicks[0][1]][0] == \
                        self.gs.board[self.playerClicks[1][0]][self.playerClicks[1][1]][0]:
                    print(" Check click is in same team")
                    self.click = self.playerClicks[1]
                    playerClicks = [self.click]
                else:
                    move = Move(self.playerClicks[0], self.playerClicks[1], self.gs.board)
                    if move in self.validMoves:
                        if move.capturedPiece == '--':
                            pygame.mixer.Sound.play(self.sound_move)
                        else:
                            pygame.mixer.Sound.play(self.sound_capture)
                        self.gs.makeMove(move)
                        print(f'I have made a {move.getNotation()}')
                        self.moveMade = True
                        self.click = ()
                        self.playerClicks = []


if __name__ == "__main__":
    gameMain = GameMain()
    gameMain.mainLoop()
