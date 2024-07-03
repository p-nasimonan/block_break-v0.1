'''
テキストとかのオブジェクトを操作することでメニューを動かせるようにしたい
'''

import app
import config

import pygame
from pygame.locals import *
import sys
import time

imgs = config.images
color = config.color
SCREEN_SIZE = config.SCREEN_SIZE
CENTSCx, CENTSCy = config.CenterScreen 
block_xy = config.block_xy
block_imgs = config.block_imgs
FPS = 60



def start(running): #開始関数

    # ------   インスタンス化　  -------
    GameScreen = app.WindowObject(SCREEN_SIZE, "ブロック崩しv0.1") #ウィンドウを作成
    world1 = app.World(stage = 1)
    MessageText = app.GameObject(world1, ReferencePos = 'center', x = CENTSCx, y =  CENTSCy) #テキスト作成
    Player = app.GameObject(world1, 200, 18, img_path = imgs['player'], ReferencePos = 'topleft', x = CENTSCx, y =  CENTSCy+100, stopk=0.9) #プレーヤー作成
    Boll = app.GameObject(world1, 50, 50, img_path = imgs['boll'], ReferencePos = 'topleft', x = CENTSCx, y =  0, vxo = config.bollvxo, vyo = config.bollvyo) #ボール作成
    Blocks = [app.GameObject(world1, config.block_sizex, config.block_sizey, img_path = block_imgs[i], ReferencePos = 'topleft', x = block_xy[i][0], y =  block_xy[i][1], vxo = config.bollvxo, vyo = config.bollvyo) for i in range(len(block_xy))] #ブロック作成

    clock = pygame.time.Clock()

    # ---- sprite ----
    move_sprites = pygame.sprite.Group()
    move_sprites.add(Player)
    move_sprites.add(Boll)

    # ---- KEYCON ----
    arrow_key = {
    K_UP: Player.up, K_DOWN: Player.down, K_RIGHT: Player.right, K_LEFT: Player.left,


    }
    # ゲームループ
    while running:
        clock.tick()
        GameScreen.screen.fill(color('black'))   # 画面を黒色で塗りつぶす
        if not world1.isstarted:
            MessageText.drawtext(GameScreen, text = 'スペースキーを押してスタート')
            MessageText.control({K_SPACE: world1.start})
        else:
            Boll.update()
            Player.update()
            Boll.draw(GameScreen)
            Player.draw(GameScreen)
            for block in Blocks:
                block.draw(GameScreen)
            Player.control(arrow_key)
            Player.physics(isstop=True)
            Boll.physics(collision=True)

        pygame.display.update()  # 画面を更新
        pygame.display.flip()
        # ---- フレームを空ける ----
        clock.tick(FPS)

    return start(True)


if __name__ == "__main__":
    start(True)