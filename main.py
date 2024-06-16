import world
import app
import config


import pygame
from pygame.locals import *
import sys
import time


def start(running): #開始関数
    GameScreen = app.WindowObject(config.SCREEN_SIZE, "ブロック崩しv0.1") #インスタンス化　ウィンドウを作成

    MessageText = app.TextObjects('center') #テキスト作成

    world.stage = 1
    player = app.GameObject('image/cloud.png', 200, 200) #プレーヤー作成
    menu = app.GameObject('image/carsol.png', 50, 50, 'center') #メニュー作成
    # ゲームループ
    while running:
        GameScreen.screen.fill(config.color['black'])   # 画面を黒色で塗りつぶす
        if not world.isstarted:
            MessageText.draw(GameScreen, 'スペースキーを押してスタート')
            player.draw(GameScreen)
            menu.draw(GameScreen)
        else:
            app.run(player, GameScreen)
        pygame.display.update()  # 画面を更新
        # イベント処理
        for event in pygame.event.get():
            if event.type == QUIT:  # 終了イベント
                pygame.quit()
                sys.exit()
            else:
                app.key(event, player) #プレイヤーのキーボード操作
                app.mouse(event, menu)
                
    return start()

if __name__ == "__main__":
    start(True)