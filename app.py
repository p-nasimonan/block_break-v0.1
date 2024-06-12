import pygame
from pygame.locals import *
import sys
import time

def player():
    pass

def key(event):
    if event.type == KEYDOWN:  # キーを押したとき
        if event.key == K_UP:
            player.up()
    # ESCキーならスクリプトを終了
        if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()