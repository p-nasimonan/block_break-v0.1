'''
次作るときは、サーフェスの作成をできるクラス作る。
Windowは一つしかできない

キーボード操作をオブジェクトで分けるのはあり
'''
import pygame
from pygame.locals import *
import sys
import time
import config
import world

#=======描画処理関数============
def ImageConvert(file_path, width=100, height=100):
    img1 = pygame.image.load(file_path)
    img2 = pygame.transform.scale(img1, (width, height))
    return img2

def rect(RefPos:str, Surface: pygame.Surface, x, y) -> pygame.Rect:
        if RefPos == 'center':
            res_rect = Surface.get_rect(center=(x, y))
        elif RefPos == 'topleft':
            res_rect = Surface.get_rect(topleft=(x, y))
        elif RefPos == 'bottomright':
            res_rect = Surface.get_rect(bottomright=(x, y))
        return res_rect



#===================ゲームオブジェクト============================
class GameObject:
    def __init__(self, img_path:str, width:int, height:int, ReferencePos:str = 'topleft', x:int = 0, y:int = 0, mousefunc:dict = {}, keyfunc:dict = {}):
        '''
        例-----------------------
        画像パス: 'image/hoge.png'
        画像幅: 100
        画像高さ: 100
        基準点: 'center' | 'topleft' | 'bottomright'
        x: 100 
        y: 100
        マウス操作{マウスの動作:実行内容}: {K_UP: self.up}
        キー設定{キー:実行内容}: {K_UP: self.up}

        '''
        self.x = x
        self.y = y
        self.image = ImageConvert(img_path, width, height)
        self.RefPos = ReferencePos
        self.keyfunc = keyfunc
        self.mousefunc = mousefunc

    #ここの関数を使って動かす
    def up(self):
        self.y -= 1
    def down(self):
        self.y += 1
    def right(self):
        self.x += 1
    def left(self):
        self.x -= 1
    def move(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self, windowobj):
        WindowObject.draw(windowobj,self)

    #操作監視-----------------------------
    def key(self, event):
        if event.type == KEYDOWN:  # キーを押したとき
            keyfunc = self.keyfunc
            #矢印キー
            for key in keyfunc:
                if event.key == key:
                    keyfunc[key]()
            if event.key == K_UP:
                self.up()
            if event.key == K_DOWN:
                self.down()
            if event.key == K_RIGHT:
                self.right()
            if event.key == K_LEFT:
                self.left()
            if event.key == K_SPACE:
                world.isstarted = True

    def mouse(self, event):
        '''
        for event in pygame.event.get():
            class.mouse(event)
        
        戻り値: マウスの座標(x, y)
        '''
        x, y = self.x, self.y
        if event.type == MOUSEMOTION:
            x, y = tuple(event.pos)
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.LeftClick()
        return x, y

    #----------------------------------
    def run(self, keyfunc):
        self.keyfunc = keyfunc
        if world.stage == 1:
            for event in pygame.event.get():
                self.key(event)
                x, y = self.mouse(event)
                self.move(x, y)

#=========スクリーンオブジェクト（作ってみたが、一個しかwindowはできないみたい。）==========
class WindowObject:
    def __init__(self, SIZE:tuple[int,int]=(480, 360), TITLE:str="タイトル未定", icon_path:str = config.images['icon']):
        # Pygameを初期化
        pygame.init()
        pygame.display.init ()

        # タイトルバーの文字列をセット
        pygame.display.set_caption(TITLE)
        #アイコンをセット
        icon = ImageConvert(icon_path)
        pygame.display.set_icon(icon)
        # SCREEN_SIZEの画面を作成
        self.screen = pygame.display.set_mode(SIZE)
        # 初期値
        self.SIZE = SIZE

    def draw(self, obj:GameObject, text:str|None = None):
        if type(text) == None:
            img_rect = rect(obj.RefPos, obj.image, obj.x, obj.y)
            self.screen.blit(obj.image, img_rect)
        else:
            img_rect = rect(obj.RefPos, obj.image, obj.x, obj.y)
            self.screen.blit(obj.image, img_rect)




    


class TextObjects:
    def __init__(self, ReferencePos:str = 'center', x:int = config.CenterScreen[0], y:int = config.CenterScreen[1], color:tuple[int, int, int] = config.color('white'), font:str = config.fonts[0], fontsize:int = 50):
        self.RefPos = ReferencePos
        self.x = x
        self.y = y
        self.color = color
        self.font = pygame.font.Font(font, fontsize)

    def draw(self, winobj:WindowObject, text:str):
            x = self.x
            y = self.y
            color = self.color
            setfont = self.font.render(text, True, color)
            text_rect = rect(self.RefPos, setfont, x, y)
            winobj.screen.blit(setfont, text_rect)




