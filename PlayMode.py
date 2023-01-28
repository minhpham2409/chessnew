import pygame
import pygame_gui.elements

from GameInit import GameInit
from config import *


class PlayMode(GameInit):

    def __init__(self, screen):
        super().__init__(screen)
        self.__loadGUI()
        self.__editPanel()

    def __loadGUI(self):
        self.label_time = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((LEFT_TIMER, TOP_TIMER), (WIDTH_LABEL, HEIGHT_LABEL)),
            text='Time: ', manager=self.manager)

        self.label_turn = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((LEFT_TURN, TOP_TURN), (WIDTH_LABEL, HEIGHT_LABEL)),
            text='Turn: ', manager=self.manager)

        self.label_possible_move = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((LEFT_POSSIBLE_MOVE, TOP_POSSIBLE_MOVE), (WIDTH_LABEL, HEIGHT_LABEL)),
            text='Possible moves: ', manager=self.manager)

        self.label_incheck = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((LEFT_INCHECK, TOP_INCHECK), (WIDTH_LABEL, HEIGHT_LABEL)),
            text='In Check : ', manager=self.manager)

    def mainLoop(self):
        self.running = True
        while self.running:
            #   Handle event
            self.__eventHandler()

            #  move update
            if self.moveMade:
                self.validMoves = self.gs.getValidMoves()
                self.__editPanel()
                self.moveMade = False

            #   Update screen
            self.setClock()
            self.__drawScreen()
            pygame.display.update()

    def __drawScreen(self):
        self.drawGameScreen()
        self.__drawPanel()
        self.screen.blit(self.panel_screen, (WIDTH, 0))

    def __drawPanel(self):
        self.manager.update(0.066)
        self.manager.draw_ui(self.panel_screen)

    def __eventHandler(self):
        for event in pygame.event.get():
            # Event occurs when click X button
            if event.type == pygame.QUIT:
                self.running = False
            # Event occurs when click into screen
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.__clickHandler()
            # Event occurs when press into a key
            elif event.type == pygame.KEYDOWN:
                # Press r to reset
                if event.key == pygame.K_r:
                    self.__reset()

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

    def __clickHandler(self):
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

    def __editPanel(self):

        self.text_box.set_text(self.gs.getMoveNotation())
        self.label_turn.set_text(self.gs.getTurn())
        self.label_possible_move.set_text(f'Possible moves: {len(self.validMoves)}')
        self.label_incheck.set_text(f'In Check : {self.gs.inCheck}')

    def setClock(self):
        time = pygame.time.get_ticks() // 1000
        min = time // 60
        sec = time % 60
        s = "%02d:%02d" % (min, sec)
        self.label_time.set_text(f"Time: {s}")

    def __reset(self):
        self.__init__(self.screen)
        print("Reset game")
