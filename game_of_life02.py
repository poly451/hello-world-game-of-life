# This is a first draft; I didn't use all he functions below.

import pygame, sys
import world01 as world
from world01 import Map, Tile
from random import randint
import time

MAPFILE = "game_of_life.txt"
TITLE = "Welcome to the Game of Life!"

class Game():
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((world.SCREENWIDTH, world.SCREENHEIGHT))
        pygame.display.set_caption(TITLE)
        self.surface.fill(world.UGLY_PINK)
        self.world_map = Map(MAPFILE, self)

    def _get_decision(self):
        d = ['above', 'below', 'right', 'left']
        ran = randint(0,3)
        return d[ran]

    def next_turn(self):
        # --------- Read patterns -------------
        # read tiles from left to right, top to bottom.
        self.world_map.examine_world()
        # -------- decision -----------------
        self.world_map.decide()

    def draw(self):
        self.world_map.draw()

    def game_loop(self):
        print("===== BEGIN WHILE LOOP ========")
        while True:
            # print("begin while loop")
            for event in pygame.event.get():
                # print("inside pygame.event.get()")
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    print("inside pygame.KEYDOWN")
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_t:
                        print("before next turn")
                        mygame.next_turn()
                        print("after next turn")
            mygame.next_turn()
            mygame.draw()
            pygame.display.update()
            time.sleep(1)
        print("===== END WHILE LOOP ========")

if __name__=="__main__":
    mygame = Game()
    mygame.draw()
    mygame.game_loop()
