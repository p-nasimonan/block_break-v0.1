import pygame
from pygame.locals import *
import sys
import time
class Window:
    def __init__(self, size:tuple[int,int]=(480, 360), title:str="タイトル未定"):
        # Pygameを初期化
        pygame.init()
        # タイトルバーの文字列をセット
        pygame.display.set_caption(title)

        # SCREEN_SIZEの画面を作成
        self.screen = pygame.display.set_mode(size)


class GameObj:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def up(self):
        self.y += 1

class textobj:
    def __init__(self, x:int, y:int, color:tuple[int]):
        self.x = x
        self.y = y
        self.color = color

def key(event, obj):
    if event.type == KEYDOWN:  # キーを押したとき
        if event.key == K_UP:
            obj.up()
    # ESCキーならスクリプトを終了
        if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()