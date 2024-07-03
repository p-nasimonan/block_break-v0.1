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
        self.objects = []  # GameObjectインスタンスを格納するリストを追加

    def start(self):
        self.isstarted = True

    def add_object(self, obj):
        self.objects.append(obj)  # GameObjectインスタンスをリストに追加



#===================ゲームオブジェクト============================
class GameObject(pygame.sprite.Sprite):
    def __init__(self, world:World, width:int|None = None, height:int|None = None, img_path:str|None = None, ReferencePos:str = 'topleft', x:int = 0, y:int = 0, gravity:bool = False, vxo = 0, vyo = 0, stopk = 0.4,va = config.PLAYER_A):
        '''
        例-----------------------
        画像パス: 'image/hoge.png'
        画像幅: 100
        画像高さ: 100
        基準点: 'center' | 'topleft' | 'bottomright'
        x: 100 
        y: 100
        初期マウス操作{マウスの動作:実行内容, 引数}: {K_UP: self.up,()}
        初期キー設定{キー:実行内容, 引数}: {K_UP: self.up,()}

        '''
        super().__init__()

        #画像が入った場合
        if img_path is not None:
            try:
                self.image = ImageConvert(img_path, width, height)
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
            except FileNotFoundError:
                raise FileNotFoundError(f'{img_path}が見つかりません')
            except:
                raise Exception('画像以外にも高さや幅を入れないといけません!')
        else:
            if width is not None and height is not None:
                self.rect = pygame.Rect(x, y, width, height)  # デフォルトのrectを設定
            else:
                self.rect = pygame.Rect(x, y, 0, 0)  # デフォルトのrectを設定

        self.x = x
        self.y = y
        self.RefPos = ReferencePos

        self.world = world
        self.world.add_object(self)  # Worldクラスのobjectsリストに自身を追加

        self.gravity = gravity
        if self.gravity:
            self.ay = config.g
        else:
            self.ay = 0
        self.ax = 0
        self.vxo = vxo
        self.vyo = vyo
        self.vy = vyo
        self.vx = vxo
        self.va = va
        self.ishit = {obj:False for obj in self.world.objects}
        self.stopk = stopk


    #ここの関数を使って動かす
    def up(self):
        self.vy -= self.va
    def down(self):
        self.vy += self.va
    def right(self):
        self.vx += self.va
    def left(self):
        self.vx -= self.va

    # change v(低速速モードなど)
    def chv(self, va):
        self.va = va
    
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
        if len(self.world.objects) > len(self.ishit):
            self.ishit[self.world.objects[-1]] = False


    # 摩擦抗力的な
    def stop(self, isstop):
        if isstop:
            if abs(self.vyo) > abs(self.vy):
                self.vy = self.vy*(2-self.stopk)
            if abs(self.vyo) < abs(self.vy):
                self.vy = self.vy*self.stopk

            if abs(self.vxo) > abs(self.vx):
                self.vx = self.vx*(2-self.stopk)
            if abs(self.vxo) < abs(self.vx):
                self.vx = self.vx*self.stopk

    # --- 物理 ---
    def physics(self, isstop:bool = False, collision:bool = False):
        # --- 当たり判定 ---
        if collision:
            new_rect = self.rect.copy()  # 予測したい
            new_rect.y += self.vy
            new_rect.x += self.vx
            for other in self.world.objects:
                if other is not self:
                    new_other_rect = other.rect.copy()
                    new_other_rect.y += other.vy
                    new_other_rect.x += other.vx
                    #自分が相手に当たるか
                    is_self_collide_other = new_rect.colliderect(new_other_rect)
                    if is_self_collide_other and not self.ishit[other]:
                        self.ishit[other] = True
                        print(self.ishit)

                        self.vy = -1 * self.vy #+ other.vy   #<-跳ね返りと相手の速度が影響されるとずっと加速していくから良くない
                        self.vx = -1 * self.vx #+ other.vx

                    else:
                        self.ishit[other] = False
                    del new_other_rect

        self.rect.y += self.vy
        self.rect.x += self.vx

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


        





    #操作監視-----------------------------
    def key(self, keyfunc:dict):
        #dictで保したキー:実行する内容
        pressed_keys = pygame.key.get_pressed()
        try:
            for key, func in keyfunc.items(): # keyfunc = {key: function}
                if pressed_keys[key]:
                    func()
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







    



