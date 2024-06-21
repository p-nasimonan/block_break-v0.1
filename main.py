'''
テキストとかのオブジェクトを操作することでメニューを動かせるようにしたい
'''

import world
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

def start(running): #開始関数
    GameScreen = app.WindowObject(SCREEN_SIZE, "ブロック崩しv0.1") #インスタンス化　ウィンドウを作成
    MessageText = app.TextObjects('center') #テキスト作成

    world.stage = 1
    player = app.GameObject(imgs['player'], 200, 200, 'center') #プレーヤー作成
    carsol = app.GameObject(imgs['carsol'], 50, 50, 'center') #カーソル作成
    # ゲームループ
    while running:
        GameScreen.screen.fill(color('black'))   # 画面を黒色で塗りつぶす
        if not world.isstarted:
            MessageText.draw(GameScreen, 'スペースキーを押してスタート')
            #ここの状態ではスペースキーだけのdictを入れるとか
            player.draw(GameScreen)
            carsol.run(GameScreen, {})
        else:
            player.run(GameScreen)
        pygame.display.update()  # 画面を更新
        # イベント処理
        for event in pygame.event.get():
            if event.type == QUIT:  # 終了イベント
                pygame.quit()
                sys.exit()
                
    return start()

if __name__ == "__main__":
    start(True)