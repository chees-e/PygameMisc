import pygame
import random

import util.const as G
from scenes import menu

class Game:
    def __init__(self, screen):
        self.screen = screen

        print("Game started")

    def run(self):
        menu.run(self.screen, {})


def main():
    pygame.init()

    pygame.display.set_caption("Blocc")
    screen = pygame.display.set_mode(G.size)
    screen.fill(G.bg_colour)

    pygame.display.flip()

    # input()

    g = Game(screen)
    # g.run()


if __name__ == "__main__":
    main()
    pygame.quit()
