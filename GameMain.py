import pygame
import pygame_gui

from config import *
import util
from GameState import GameState


class GameMain:
    def __init__(self, screen: pygame.Surface):

        self.screen = screen

        self.IMAGES = {}
        self.__loadImages()
        self.__loadSound()

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

    def mainLoop(self):
        self.running = True
        while self.running:
            self.time_delta = self.clock.tick(MAX_FPS) / 1000

            #   Handle event
            self.eventHandler()

            #  move update
            if self.moveMade:
                s = self.gs.getMoveNotation()
                self.text_box.set_text(html_text=s)
                self.moveMade = False
                self.validMoves = self.gs.getValidMoves()

            #   Update screen
            self.drawScreen()
            pygame.display.update()

    # Load images into memory
    def __loadImages(self):
        pieces = ['wp', 'wR', 'wN', 'wB', 'wK',
                  'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
        for piece in pieces:
            self.IMAGES[piece] = pygame.transform.scale(pygame.image.load(f"data/images/{piece}.png"),
                                                        (SQ_SIZE, SQ_SIZE))

    # Load sound into memory
    def __loadSound(self):
        self.sound_move = pygame.mixer.Sound('data/sound/move.wav')
        self.sound_capture = pygame.mixer.Sound('data/sound/capture.wav')

    def drawScreen(self):
        self.drawBoard()
        self.drawPiece()
        self.highlightSquares()
        self.drawPanel()
        self.screen.blit(self.board_screen, (0, 0))
        self.screen.blit(self.panel_screen, (WIDTH, 0))

    def drawBoard(self):
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                color = colorBoard[(i + j) % 2]
                x = i * SQ_SIZE
                y = j * SQ_SIZE
                pygame.draw.rect(self.board_screen, color, pygame.Rect(x, y, SQ_SIZE, SQ_SIZE))

    def drawPiece(self):
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                piece = self.gs.board[i][j]
                if piece != "--":
                    self.board_screen.blit(self.IMAGES[piece], pygame.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    def highlightSquares(self):
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

    def drawPanel(self):
        self.manager.update(self.time_delta)
        self.manager.draw_ui(self.panel_screen)

    def eventHandler(self):
        for event in pygame.event.get():
            # Event occurs when click X button
            if event.type == pygame.QUIT:
                self.running = False
            # Event occurs when click into screen
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.clickHandler()
            # Event occurs when press into a key
            elif event.type == pygame.KEYDOWN:
                # Press r to reset
                if event.key == pygame.K_r:
                    self.reset()

                # Press z to undo
                if event.key == pygame.K_z:
                    self.gs.undoMove()
                    self.moveMade = True

                if event.key == pygame.K_u:
                    i = 1
                    for c in self.gs.castle_rights_log:
                        print(i, c.wqs, c.wks, c.bqs, c.bks, c, sep='::')
                        i += 1

                if event.key == pygame.K_k:
                    c = self.gs.current_castling_rights
                    print("current: ", c.wqs, c.wks, c.bqs, c.bks, c, sep='::')

    def clickHandler(self):
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
                id_click = 1000 * self.playerClicks[0][0] + 100 * self.playerClicks[0][1] + 10 * self.playerClicks[1][
                    0] + self.playerClicks[1][1]
                for move in self.validMoves:
                    if move.moveID == id_click:
                        if move.capturedPiece == '--':
                            pygame.mixer.Sound.play(self.sound_move)
                        else:
                            pygame.mixer.Sound.play(self.sound_capture)
                        self.gs.makeMove(move)
                        self.moveMade = True
                        break

                self.click = ()
                self.playerClicks = []

    def reset(self):
        self.__init__(self.screen)
        print("Reset game")
