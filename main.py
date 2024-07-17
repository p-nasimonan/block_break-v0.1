'''
テキストとかのオブジェクトを操作することでメニューを動かせるようにしたい
'''

from app import app
from app import config

import pygame
from pygame.locals import *
import sys
import time

imgs = config.images
color = config.color
SCREEN_SIZE = config.SCREEN_SIZE
CENTSCx, CENTSCy = config.CenterScreen 
FPS = config.FPS

# ------   インスタンス化　  -------
GameScreen = app.WindowObject(SCREEN_SIZE, "ブロック崩しv0.1") #ウィンドウを作成
Menu = app.World(stage=0)
MessageText = app.GameObject(Menu, ReferencePos = 'center', x = CENTSCx, y =  CENTSCy) #テキスト作成
# ワールドの作成
World1 = app.World(stage = 1)
World2 = app.World(stage = 2)
World3 = app.World(stage = 3)

World_list = [World1, World2, World3]

def display_update(f):
    def _wrapper(*args):
        while True:
            # 前処理
            clock = pygame.time.Clock()
            clock.tick()


            # デコレート対象の関数の実行
            re_val = f(*args)

            # 後処理

            pygame.display.update()  # 画面を更新
            pygame.display.flip()
            clock.tick(FPS) #フレームをFPSに従って開ける
            GameScreen.screen.fill(color('black'))   # 画面を黒色で塗りつぶす

            if re_val != None:
                return re_val
    return _wrapper



@display_update
def menu():
    MessageText.drawtext(GameScreen, text = 'スペースキーを押してスタート', x = CENTSCx, y = CENTSCy)
    MessageText.drawtext(GameScreen, text = '操作方法',RefPos='topleft', x = CENTSCx- 600, y = CENTSCy+170, fontsize = 30)
    MessageText.drawtext(GameScreen, text = '十字キーで移動',RefPos='topleft', x = CENTSCx-600, y = CENTSCy+220, fontsize = 20)
    MessageText.drawtext(GameScreen, text = 'シフトキーで低速モード',RefPos='topleft', x = CENTSCx-600, y = CENTSCy+250, fontsize = 20)
    MessageText.control({K_SPACE: World1.start, K_1: World2.start})
    if World1.isstarted:
        return World_list.index(World1)
    if World2.isstarted:
        return World_list.index(World2)
    
        

def stage_init(world) -> tuple[app.GameObject, dict, app.GameObject, list[app.GameObject]]:
    Player = app.GameObject(world, 200, 5, img_path = imgs['player'], ReferencePos = 'topleft', x = CENTSCx, y =  CENTSCy+100, stopk=0.1) #プレーヤー作成
    Boll = app.GameObject(world, 50, 50, img_path = imgs['boll'], ReferencePos = 'topleft', x = CENTSCx, y =  CENTSCy, vxo = config.bollvxo, vyo = config.bollvyo) #ボール作成
    Blocks = [app.GameObject(world, config.block_sizex, config.block_sizey, img_path = world.block_imgs[i], ReferencePos = 'topleft', x = world.block_xy[i][0], y =  world.block_xy[i][1], deltable = True) for i in range(len(world.block_xy))] #ブロック作成


    # ---- KEYCON ----
    player_key = {
        K_RIGHT: Player.right, K_LEFT: Player.left,
        K_LSHIFT: ({Player.chv: 1}, {Player.chv: 5})
    }
    return Player, player_key, Boll, Blocks

@display_update
def stage(Player, player_key, Boll, Blocks):
    
    #独自の更新処理
    Boll.update()
    Player.update()

    # --- 描画 ---
    Boll.draw(GameScreen)
    Player.draw(GameScreen)

    # --- ブロックを消す処理 ---
    #これから消すブロックを初期化
    del_blocks = [] 
    
    #一旦消すブロックを保存
    for block in Blocks:
        if block.is_show:
            block.draw(GameScreen)
        else:
            del_blocks.append(block)

    #一気に消す
    for block in del_blocks:
        Blocks.remove(block)
    
    if len(Blocks) == 0:
        return 0


    # --- 操作 ---
    Player.control(player_key)

    # --- 物理 ---
    Player.physics(isstop=True)
    Boll.physics(collision=True)

def start(): #開始関数
    world_index = menu()
    for _ in range(len(World_list)-world_index):
        Player, player_key, Boll, Blocks  = stage_init(World_list[world_index])
        stage(Player, player_key, Boll, Blocks)
        world_index += 1


if __name__ == "__main__":
    start()