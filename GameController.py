from GameMain import GameMain
import pygame

from MenuScreen import MenuScreen
from PlayMode import PlayMode
from config import *


class GameController:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Cờ vua AI")
        self.icon = pygame.image.load('assets/images/icon.jpg')

        pygame.display.set_icon(self.icon)
        self.screen = pygame.display.set_mode((WIDTH_WINDOW, HEIGHT_WINDOW))

    def run(self):
        # Entry point for game
        self.__inMenuScreen()

    def __inMenuScreen(self):
        menuScreen = MenuScreen(self.screen)

        # Apply function handler for each button
        menuScreen.menu.get_widget('PvP').set_onreturn(self.__inPlayScreen)
        menuScreen.menu.get_widget('PvC').set_onreturn(self.__inPlayAIScreen)
        print("i am in menu screen")

        # Start menu loop
        menuScreen.mainLoop()
        print("I am exiting menu")

    def __inPlayScreen(self):
        playMode = PlayMode(self.screen)
        playMode.mainLoop()

    def __inPlayAIScreen(self):
        pass


if __name__ == "__main__":
    game = GameController()
    game.run()
