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
import numpy as np

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
    def __init__(self, world:World, width:int|None = None, height:int|None = None, img_path:str|None = None, ReferencePos:str = 'topleft', x:int = 0, y:int = 0, gravity:bool = False, vyo = 0):
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
        self.gravity = gravity
        if self.gravity:
            self.ay = config.g
        else:
            self.ay = 0
        self.vyo = vyo
        self.vy = vyo
        self.vx = 0
        self.v = np.array([self.vx, self.vy])
        self.ishit = False
        self.stopv = 0.5

    #ここの関数を使って動かす
    def up(self):
        self.vy -= 5
    def down(self):
        self.vy += 5
    def right(self):
        self.vx += 5
    def left(self):
        self.vx -= 5
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

    def stop(self, isstop):
        if isstop:
            self.vy = self.vy*self.stopv
            self.vx = self.vx*self.stopv

    # --- 物理 ---
    def physics(self, isstop:bool = False):
        # --- 積分...ではないか ---
        self.rect.y +=  self.vy
        self.rect.x +=  self.vx

        self.stop(isstop)

        # ---- 画面の端に当たった時の処理 -----
        # player.rectの右が画面幅より大きい場合
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.vx = -1 * self.vx
        if self.rect.left < 0:
            self.rect.left = 0
            self.vx = -1 * self.vx
        
        #高さも同様
        if self.rect.bottom > HIGHT:
            self.rect.bottom = HIGHT
            self.vy = -1 * self.vy
        if self.rect.top < 0:
            self.rect.top = 0
            self.vy = -1 * self.vy


     # --- 当たり判定 ---
    def collision(self, other) -> bool:
        #ndarrayに変換
        o_topleft = np.array(other.rect.topleft).reshape(2, 1)
        s_topleft = np.array(self.rect.topleft).reshape(2, 1)
        o_top= np.array([other.rect.centerx, other.rect.top]).reshape(2, 1)
        s_top = np.array([self.rect.centerx,self.rect.top]).reshape(2, 1)
        o_topright = np.array(other.rect.topright).reshape(2, 1)
        s_topright = np.array(self.rect.topright).reshape(2, 1)

        o_left = np.array([other.rect.left, other.rect.centery]).reshape(2, 1)
        s_left = np.array([self.rect.left, self.rect.centery]).reshape(2, 1)
        o_right= np.array([other.rect.right, other.rect.centery]).reshape(2, 1)
        s_right = np.array([self.rect.right, self.rect.centery]).reshape(2, 1)

        o_bottomleft = np.array(other.rect.bottomleft).reshape(2, 1)
        s_bottomleft = np.array(self.rect.bottomleft).reshape(2, 1)
        o_bottom = np.array([other.rect.centerx, other.rect.bottom]).reshape(2, 1)
        s_bottom = np.array([self.rect.centerx, self.rect.bottom]).reshape(2, 1)
        o_bottomright = np.array(other.rect.bottomright).reshape(2, 1)
        s_bottomright = np.array(self.rect.bottomright).reshape(2, 1)

        #自分が相手の当たり判定に入ったか
        is_self_in_other = all(o_topleft < s_bottomright) and all(s_topleft < o_bottomright)
        # どこに自分があったか(当たってる前提)
        def where_self_hit():
            self_allpos = np.concatenate([s_topleft,s_top,s_topright, s_left,s_right, s_bottomleft,s_bottom,s_bottomright], 1)
            other_allpos = np.concatenate([o_topleft,o_top,o_topright, o_left,o_right, o_bottomleft,o_bottom,o_bottomright], 1)
            pos_diff = other_allpos - self_allpos
            print(other_allpos)
            print(self_allpos)
            print(pos_diff)
            print(np.argmin(pos_diff,1))
            allpos_index = np.unravel_index(np.argmin(pos_diff,1), pos_diff.shape)
            print(self_allpos[allpos_index])
            result = 0
            return result
        

        if is_self_in_other and not self.ishit:
            where_self_hit()
            self.ishit = True
            #跳ね返り
            self.vy = -1 * self.vy
            
            #範囲外に追い出す
            self.rect.y += self.vy * 5
        else:
            self.ishit = False

        return self.ishit



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







    


