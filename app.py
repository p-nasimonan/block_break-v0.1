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

WIDTH, HIGHT = config.SCREEN_SIZE

#=======描画処理関数============
def ImageConvert(file_path, width=100, height=100):
    img = pygame.image.load(file_path)
    tranced_img2 = pygame.transform.scale(img, (width, height))
    return tranced_img2

def rect(RefPos:str, Surface: pygame.Surface, x, y) -> pygame.Rect:
        if RefPos == 'center':
            res_rect = Surface.get_rect(center=(x, y))
        elif RefPos == 'topleft':
            res_rect = Surface.get_rect(topleft=(x, y))
        elif RefPos == 'bottomright':
            res_rect = Surface.get_rect(bottomright=(x, y))
        return res_rect

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


class World:
    def __init__(self, isstarted:bool = False, stage:int = 1):
        self.isstarted = isstarted
        self.stage = stage
    
    def start(self):
        self.isstarted = True



#===================ゲームオブジェクト============================
class GameObject(pygame.sprite.Sprite):
    def __init__(self, world:World, width:int|None = None, height:int|None = None, img_path:str|None = None, ReferencePos:str = 'topleft', x:int = 0, y:int = 0):
        '''
        例-----------------------
        画像パス: 'image/hoge.png'
        画像幅: 100
        画像高さ: 100
        基準点: 'center' | 'topleft' | 'bottomright'
        x: 100 
        y: 100
        初期マウス操作{マウスの動作:実行内容}: {K_UP: self.up}
        初期キー設定{キー:実行内容}: {K_UP: self.up}

        '''
        super().__init__()
        if not width == None or not height == None or not img_path == None:
            self.image = ImageConvert(img_path, width, height)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        self.x = x
        self.y = y
        self.RefPos = ReferencePos
        self.world = world

    #ここの関数を使って動かす
    def up(self):
        self.rect.y -= 5
    def down(self):
        self.rect.y += 5
    def right(self):
        self.rect.x += 5
    def left(self):
        self.rect.x -= 5
    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y
    def LeftClick(self):
        pass
    
    # ----- 描画 ------
    def draw(self, winobj:WindowObject):
        img_rect = rect(self.RefPos, self.image, self.rect.x, self.rect.y)
        winobj.screen.blit(self.image, img_rect)
    
    def drawtext(self, winobj:WindowObject, text:str|None = None, color:tuple[int, int, int] = config.color('white'), font:str = config.fonts[0], fontsize:int = 50):
        pyfont = pygame.font.Font(font, fontsize)
        setfont = pyfont.render(text, True, color)
        img_rect = rect(self.RefPos, setfont, self.x, self.y)
        winobj.screen.blit(setfont, img_rect)

    # --- 常にやる処理 -----
    def update(self):
        super().update()

    # --- 物理 ---
    def physics(self):
        # player.rectの右が画面幅より大きい場合
        if self.rect.right > WIDTH:
            # player.rectのrightは画面幅になる（つまり止まる）
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        
        #高さも同様
        if self.rect.bottom > HIGHT:
            self.rect.bottom = HIGHT
        if self.rect.top < 0:
            self.rect.top = 0
    #操作監視-----------------------------
    def key(self, keyfunc:dict):
        #dictで保存したキー:実行する内容
        pressed_keys = pygame.key.get_pressed()
        try:
            for key in keyfunc:
                if pressed_keys[key]:
                    keyfunc[key]()
        except:
            pass

    def mouse(self, event, mousefunc:dict):
        x, y = self.rect.x, self.rect.y
        if event.type == MOUSEMOTION:
            x, y = tuple(event.pos)
            self.move(x, y)
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                x, y = tuple(event.pos)
                self.LeftClick()
        

    #操作する--------------
    def control(self, keyfunc:dict[int, object] ={}, mousefunc:dict[int, object] = {}):
        '''
        pygame.event.get()を使ってeventを取得する。get()を使った後eventは消えるため注意
        '''
        self.key(keyfunc)
        for event in pygame.event.get():   
            if not mousefunc == {}:
                self.mouse(event, mousefunc)

            if event.type == QUIT:  # 終了イベント
                    pygame.quit()
                    sys.exit()







    


