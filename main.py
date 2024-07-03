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
FPS = 60



def start(running): #開始関数

    # ------   インスタンス化　  -------
    GameScreen = app.WindowObject(SCREEN_SIZE, "ブロック崩しv0.1") #ウィンドウを作成
    world1 = app.World(stage = 1)
    MessageText = app.GameObject(world1, ReferencePos = 'center', x = CENTSCx, y =  CENTSCy) #テキスト作成
    Player = app.GameObject(world1, 200, 5, img_path = imgs['player'], ReferencePos = 'topleft', x = CENTSCx, y =  CENTSCy+100, stopk=0.9) #プレーヤー作成
    Boll = app.GameObject(world1, 50, 50, img_path = imgs['boll'], ReferencePos = 'topleft', x = CENTSCx, y =  CENTSCy+50, vxo = config.bollvxo, vyo = config.bollvyo) #ボール作成
    Blocks = [app.GameObject(world1, config.block_sizex, config.block_sizey, img_path = world1.block_imgs[i], ReferencePos = 'topleft', x = world1.block_xy[i][0], y =  world1.block_xy[i][1], deltable = True) for i in range(len(world1.block_xy))] #ブロック作成

    clock = pygame.time.Clock()

    # ---- sprite ----
    move_sprites = pygame.sprite.Group()
    move_sprites.add(Player)
    move_sprites.add(Boll)

    # ---- KEYCON ----
    player_key = {
    K_RIGHT: Player.right, K_LEFT: Player.left,
    K_LSHIFT: ({Player.chv: 1}, {Player.chv: 5})

    }
    # ゲームループ
    while running:
        clock.tick()
        GameScreen.screen.fill(color('black'))   # 画面を黒色で塗りつぶす
        if not world1.isstarted:
            MessageText.drawtext(GameScreen, text = 'スペースキーを押してスタート', x = CENTSCx, y = CENTSCy)
            MessageText.drawtext(GameScreen, text = '操作方法',RefPos='topleft', x = CENTSCx- 600, y = CENTSCy+170, fontsize = 30)
            MessageText.drawtext(GameScreen, text = '十字キーで移動',RefPos='topleft', x = CENTSCx-600, y = CENTSCy+220, fontsize = 20)
            MessageText.drawtext(GameScreen, text = 'シフトキーで低速モード',RefPos='topleft', x = CENTSCx-600, y = CENTSCy+250, fontsize = 20)
            MessageText.control({K_SPACE: world1.start})
        else:
            Boll.update()
            Player.update()

            # --- 描画 ---
            Boll.draw(GameScreen)
            Player.draw(GameScreen)
            for block in Blocks:
                if block.is_show:
                    block.draw(GameScreen)

            # --- 操作 ---
            Player.control(player_key)

            # --- 物理 ---
            Player.physics(isstop=True)
            Boll.physics(collision=True)

        pygame.display.update()  # 画面を更新
        pygame.display.flip()
        clock.tick(FPS) #フレームをFPSに従って開ける

    return start(True)


if __name__ == "__main__":
    start(True)