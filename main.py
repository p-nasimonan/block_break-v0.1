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
FPS = 60



def start(running): #開始関数
    GameScreen = app.WindowObject(SCREEN_SIZE, "ブロック崩しv0.1") #インスタンス化　ウィンドウを作成
    world1 = app.World(stage = 1)
    MessageText = app.GameObject(world1, ReferencePos = 'center', x = CENTSCx, y =  CENTSCy) #テキスト作成
    Player = app.GameObject(world1, 100, 18, imgs['player'], ReferencePos = 'topleft', x = CENTSCx, y =  CENTSCy) #プレーヤー作成
    # ---- SPRITES:  ----
    move_sprites = pygame.sprite.Group()
    move_sprites.add(Player)
    clock = pygame.time.Clock()

    # ---- KEYCON ----
    arrow_key = {
    K_UP: Player.up, K_DOWN: Player.down, K_RIGHT: Player.right, K_LEFT: Player.left
    }
    # ゲームループ
    while running:
        clock.tick()
        GameScreen.screen.fill(color('black'))   # 画面を黒色で塗りつぶす
        move_sprites.update()
        if not world1.isstarted:
            MessageText.drawtext(GameScreen, text = 'スペースキーを押してスタート')
            MessageText.control({K_SPACE: world1.start})
        else:
            Player.draw(GameScreen)
            Player.control(arrow_key)
            Player.physics()
        pygame.display.update()  # 画面を更新
        pygame.display.flip()
        # ---- フレームを空ける ----
        clock.tick(FPS)

    return start(True)


if __name__ == "__main__":
    start(True)