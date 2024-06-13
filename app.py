import pygame
from pygame.locals import *
import sys
import time

class gameobj:
    def __init__(self):
        self.x = 0
        self.y = 0
    def up(self):
        self.y += 1
        

def key(event, player):
    if event.type == KEYDOWN:  # キーを押したとき
        if event.key == K_UP:
            player.up()
    # ESCキーならスクリプトを終了
        if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()