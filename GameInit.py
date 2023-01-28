import pygame
import pygame_gui

from GameState import GameState
from config import *


class GameInit:
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
        self.manager = pygame_gui.UIManager((WIDTH_PANEL, HEIGHT_PANEL),theme_path="theme_custom.json")
        self.text_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((LEFT_MOVE_BOX, TOP_MOVE_BOX), (WIDTH_MOVE_BOX, HEIGHT_MOVE_BOX)),
            html_text='',
            manager=self.manager,
        )

        self.gs = GameState()
        self.clock = pygame.time.Clock()

        self.click = ()  # Represent location of square which is pushed by mouse
        self.playerClicks = []
        self.moveMade = False
        self.validMoves = self.gs.getValidMoves()
        self.running = True

    def __loadImages(self):
        pieces = ['wp', 'wR', 'wN', 'wB', 'wK',
                  'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
        for piece in pieces:
            self.IMAGES[piece] = pygame.transform.scale(pygame.image.load(f"./assets/images/{piece}.png"),
                                                        (SQ_SIZE, SQ_SIZE))

    # Load sound into memory
    def __loadSound(self):
        self.sound_move = pygame.mixer.Sound('./assets/sound/move.wav')
        self.sound_capture = pygame.mixer.Sound('./assets/sound/capture.wav')

    def drawGameScreen(self):
        self.drawBoard()
        self.drawPiece()
        self.highlightSquares()
        self.screen.blit(self.board_screen, (0, 0))

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

