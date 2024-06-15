import world
import app
import config


import pygame
from pygame.locals import *
import sys
import time


def start(): #開始関数
    GameScreen = app.WindowObject(config.SCREEN_SIZE, "ブロック崩しv0.1") #インスタンス化　ウィンドウを作成
    

    MessageText = app.textobjects(config.CenterScreen)
    print(config.CenterScreen)

    time.sleep(0.5)
    world.stage = 1
    player = app.GameObject('image/cloud', GameScreen) #インスタンス化　プレーヤー
    # ゲームループ
    while True:
        GameScreen.screen.fill(config.color['black'])   # 画面を黒色で塗りつぶす
        if not world.isstarted:
            MessageText.draw(GameScreen, 'スペースキーを押してスタート')
        else:
            app.run(player, GameScreen)

        pygame.display.update()  # 画面を更新
        # イベント処理
        for event in pygame.event.get():
            app.key(event, player) #キーボード処理
            if event.type == QUIT:  # 終了イベント
                pygame.quit()
                sys.exit()
                

if __name__ == "__main__":
    start()