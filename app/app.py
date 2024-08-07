'''
Windowは一つしかできない

GameObject:ゲームに表示するスプライト全般を作れる
    update()は必須
    control()はキーボードとマウスの操作をする。
    physics()は物理演算をする。
    draw()は描画をする。

World:ゲームの世界を作れる。
    start()はゲームを開始する。
    add_object()はゲームオブジェクトを追加する。(GameObjectのinitに含まれている)
'''
import pygame
from pygame.locals import *
import sys
import time
import random
import math
import app.config as config
delta_time = config.delta_time


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
    """ワールド(ゲームのステージ)
    Attributes:
        __init__: ブロックのデータをファイルから読み取り、生成
        start: ステージを開始する
        add_object: ブロックとかボールとかプレイヤーをこのワールドのobjectに追加しておく。

    """
    def __init__(self, isstarted:bool = False, stage:int = 1):
        """初期化
        Args:
            isstarted: 開始したか
        
        """
        self.isstarted = isstarted
        self.stage = stage
        file = config.open_stage(stage)
        self.block_xy, self.block_imgs = config.blocklist_convert(file)
        self.objects:list[GameObject] = []  # GameObjectインスタンスを格納するリストを追加

    def start(self):
        self.isstarted = True

    def add_object(self, obj):
        self.objects.append(obj)  # GameObjectインスタンスをリストに追加



#===================ゲームオブジェクト============================
class GameObject(pygame.sprite.Sprite):
    def __init__(self, world:World, width:int|None = None, height:int|None = None, img_path:str|None = None, ReferencePos:str = 'topleft', x:int = 0, y:int = 0, gravity:bool = False, vxo = 0, vyo = 0, stopk = 0.4,va = config.PLAYER_A, deltable:bool = False, is_show:bool = True):
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
        self.ishit = {obj:False for obj in self.world.objects} #全てのオブジェクトとの当たり判定をFalseにする
        self.stopk = stopk
        self.deltable = deltable
        self.is_show = is_show


    #=============   操作する関数   =====================
    def up(self):
        self.vy -= self.va * delta_time
    def down(self):
        self.vy += self.va * delta_time
    def right(self):
        self.vx += self.va * delta_time
    def left(self):
        self.vx -= self.va * delta_time

    # change v(低速速モードなど)
    def chv(self, va):
        self.va = va
    
    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y
    def LeftClick(self):
        pass

    def kill(self):
        self.is_show = False
        self.world.objects.remove(self)

    

    # ========= 描画 =========
    def draw(self, winobj:WindowObject):
        if self.is_show:
            img_rect = rect(self.RefPos, self.image, self.rect.x, self.rect.y)
            winobj.screen.blit(self.image, img_rect)
    
    def drawtext(self, winobj:WindowObject, text:str, x:int|None = None, y:int|None = None, RefPos:str|None = None, color:tuple[int, int, int] = config.color('white'), font:str = config.fonts[0], fontsize:int = 50):
        if self.is_show:
            if x is None:
                x = self.x
            if y is None:
                y = self.y
            if RefPos is None:
                RefPos = self.RefPos
            pyfont = pygame.font.Font(font, fontsize)
            setfont = pyfont.render(text, True, color)
            img_rect = rect(RefPos, setfont, x, y)
            winobj.screen.blit(setfont, img_rect)

    # ========= 常にやる処理 =========
    def update(self):
        if self.is_show:
            super().update()
            if len(self.world.objects) > len(self.ishit):
                self.ishit[self.world.objects[-1]] = False
            else:
                for obj in self.world.objects:
                    if not obj.is_show:
                        self.world.objects.remove(obj)


    #=============   物理   =====================
    # 摩擦的な
    def stop(self, isstop):
        if isstop:
            self.vy *= max(0, 1 - self.stopk / delta_time)
            self.vx *= max(0, 1 - self.stopk / delta_time)

    # --- 当たり判定 ---
    def collision(self):
            #移動後の位置を計算
            new_rect = self.rect.copy()  
            new_rect.y += self.vy * delta_time
            new_rect.x += self.vx * delta_time
            for other in self.world.objects:
                if other is not self:
                    #移動後の相手の位置を計算
                    new_other_rect = other.rect.copy()
                    new_other_rect.y += other.vy * delta_time   
                    new_other_rect.x += other.vx * delta_time
                    
                    #自分が相手に当たるか
                    new_is_self_collide_other = new_rect.colliderect(new_other_rect)
                    if new_is_self_collide_other and not self.ishit[other]:
                        if other.deltable:
                            other.kill()
                        self.ishit[other] = True

                        if self.vx > self.vy:
                            self.vx = -1 * self.vx
                        if self.vx < self.vy:
                            self.vy = -1 * self.vy

                        #後ずけの防止対策よりも先にこの状況になることを防ぎたい

                    else:
                        self.ishit[other] = False
    

    # --- 物理 ---
    def physics(self, isstop:bool = False, collision:bool = False):
        if self.is_show:    
            # --- 当たり判定 ---
            if collision:
                self.collision()    

            # --- 位置調整 ---
            self.rect.y += self.vy * delta_time
            self.rect.x += self.vx * delta_time

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


    #=============   操作   =====================
    def key(self, keyfunc:dict):
        #dictで保したキー:実行する内容
        pressed_keys = pygame.key.get_pressed()

        for key, funcs in keyfunc.items(): # keyfunc = {key: ({func: arg}, {default_function: arg})}
            # キーが押されたら
            if pressed_keys[key]:

                # 関数に引数をつける場合
                if isinstance(funcs, tuple):
                    for function, arg in funcs[0].items():
                        function(arg)
                else:
                    funcs()
            
            # キーが離されたら
            else:
                # 関数に引数をつける場合
                if isinstance(funcs, tuple):   
                    for function, arg in funcs[1].items():
                        function(arg)


    def mouse(self, event, mousefunc:dict):
        x, y = self.rect.x, self.rect.y
        if event.type == MOUSEMOTION:
            x, y = tuple(event.pos)
            self.move(x, y)
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                x, y = tuple(event.pos)
                self.LeftClick()
        
    args = None|int|str
    #操作する--------------
    def control(self, keyfunc:dict[int, tuple[dict[object, args], dict[object, args]]] ={}, mousefunc:dict[int, object] = {}):
        '''
        keyfuncには、キーと関数を格納する。
        例: {K_UP: ({self.function: 5}, {self.function: 1})}
        キーが押されたら、self.function(5)が実行される。
        キーが離されたら、self.function(1)が実行される。

        mousefuncには、マウスと関数を格納する。
        pygame.event.get()を使ってeventを取得する。get()を使った後eventは消えるため注意
        '''
        if self.is_show:
            self.key(keyfunc)

            for event in pygame.event.get():   
                if not mousefunc == {}:
                    self.mouse(event, mousefunc)

                if event.type == QUIT:  # 終了イベント
                    pygame.quit()
                    sys.exit()







    



