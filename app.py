import pygame
from pygame.locals import *
import sys
import time
import config
import world

class WindowObject:
    def __init__(self, SIZE:tuple[int,int]=(480, 360), TITLE:str="タイトル未定"):
        # Pygameを初期化
        pygame.init()
        pygame.display.init ()
        # タイトルバーの文字列をセット
        pygame.display.set_caption(TITLE)
        # SCREEN_SIZEの画面を作成
        self.screen = pygame.display.set_mode(SIZE)
        # 初期値
        self.SIZE = SIZE



#プレイヤーとかブロックとかを置く予定
class GameObject:
    def __init__(self, img, x:int = 0, y:int = 0):
        self.x = x
        self.y = y
        self.image = img
    def up(self):
        self.y += 1
    def down(self):
        self.y -= 1
    def right(self):
        self.x += 1
    def left(self):
        self.x -= 1

    def draw(self, winobj:WindowObject):
        winobj.screen.blit(self.image, (self.x, self.y))

class textobjects:
    def __init__(self, cent:tuple[int, int] = config.CenterScreen, x:int = 0, y:int = 0, color:tuple[int] = config.color['white'], font:str = config.fonts[0], fontsize:int = 50):
        self.cent = cent
        self.x = x
        self.y = y
        self.color = color
        self.font = pygame.font.Font(font, fontsize)

    def draw(self, winobj:WindowObject, text:str, x:int = None, y:int = None, color:tuple[int] = None):
            if x == None:
                x = self.x
            if y == None:
                y = self.y
            if color == None:
                color = self.color
            cent = self.cent
            setfont = self.font.render(text, True, color)
            text_rect = setfont.get_rect(center=(cent))
            winobj.screen.blit(setfont, text_rect)

def key(event, obj):
    if event.type == KEYDOWN:  # キーを押したとき
        
        #矢印キー
        if event.key == K_UP:
            obj.up()
        if event.key == K_DOWN:
            obj.down()
        if event.key == K_RIGHT:
            obj.right()
        if event.key == K_LEFT:
            obj.left()

        if event.key == K_SPACE:
            world.isstarted = True

def run(PlayObject:GameObject, winobj:WindowObject):
    if world.stage == 1:
        PlayObject.draw(winobj)
