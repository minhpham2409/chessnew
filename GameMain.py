import pygame
import pygame_gui

from config import *
import util
from GameState import GameState, Move


class GameMain:
    def __init__(self, screen: pygame.Surface):

        self.screen = screen

        self.IMAGES = {}
        self._loadImages()
        self._loadSound()

        # Surface for board game
        self.board_screen = pygame.Surface((WIDTH, HEIGHT))
        # Surface for game status and controller
        self.panel_screen = pygame.Surface((WIDTH_PANEL, HEIGHT))
        #   ---------------------------------- GUI ----------------------------------   #
        self.manager = pygame_gui.UIManager((WIDTH_PANEL, HEIGHT_PANEL))

        self.text_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((0, 0), (WIDTH_MOVE_BOX, HEIGHT_MOVE_BOX)),
            html_text='',
            manager=self.manager,
            )


        # self.button1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(0,HEIGHT_PANEL*7/8,WIDTH_PANEL/4,WIDTH_PANEL/4),
        #                                             text='',
        #                                             manager=self.manager)

        #   ---------------------------------- GUI ----------------------------------   #

        self.gs = GameState()
        self.clock = pygame.time.Clock()

        self.click = ()  # Represent location of square which is pushed by mouse
        self.playerClicks = []
        self.moveMade = False
        self.validMoves = self.gs.getValidMoves()
        self.running = True
        self.isYielding = False

    def mainLoop(self):
        self.running = True
        while self.running:
            self.time_delta = self.clock.tick(MAX_FPS) / 1000

            #   Handle event
            self._eventHandler()

            #  move update
            if self.moveMade:
                s = self.gs.getMoveNotation()
                self.text_box.set_text(html_text=s)
                self.moveMade = False
                self.validMoves = self.gs.getValidMoves()

            #   Update screen
            self._drawScreen()
            pygame.display.update()

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
        self.manager.update(self.time_delta)
        self.manager.draw_ui(self.panel_screen)

    def _eventHandler(self):
        for event in pygame.event.get():
            # Event occurs when click X button
            if event.type == pygame.QUIT:
                self.running = False
            # Event occurs when click into screen
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._clickHandler()
            # Event occurs when press into a key
            elif event.type == pygame.KEYDOWN:
                # Press r to reset
                if event.key == pygame.K_r:
                    self._reset()

                # Press g to yielding
                if event.key == pygame.K_g:
                    self._yielding()

                # Press z to undo
                if event.key == pygame.K_z:
                    self.gs.undoMove()
                    self.moveMade = True
                # Press q to log game_status
                if event.key == pygame.K_q:
                    util.logGameStatus(self.gs.capturedPieces)

                if event.key == pygame.K_l:
                    kingMoves = self.gs.getValidMoves()

                if event.key == pygame.K_u:
                    util.printBoard(self.gs.board)


    def _clickHandler(self):
        pos = pygame.mouse.get_pos()
        x = int(pos[1] / SQ_SIZE)
        y = int(pos[0] / SQ_SIZE)

        # Check valid screen
        if x in range(8) and y in range(8):

            # case when first click is empty piece or another team
            # or first click same as second click
            if self.click == (x, y) or (not self.click and (
                    self.gs.board[x][y] == '--' or self.gs.board[x][y][0] != self.gs.turn)):
                # print('Reset click')
                self.click = ()
                self.playerClicks = []
            else:
                self.click = (x, y)
                self.playerClicks.append(self.click)

            if len(self.playerClicks) == 2:
                move = Move(self.playerClicks[0], self.playerClicks[1], self.gs.board)
                if move in self.validMoves:
                    if move.capturedPiece == '--':
                        pygame.mixer.Sound.play(self.sound_move)
                    else:
                        pygame.mixer.Sound.play(self.sound_capture)
                    self.gs.makeMove(move)
                    self.moveMade = True

                self.click = ()
                self.playerClicks = []

    def _reset(self):
        self.__init__(self.screen)
        print("Reset game")

    def _yielding(self):
        self.running = False
        self.isYielding = True
        print("yielding")
