import world
import app
import config
import window

import pygame
from pygame.locals import *
import sys
import time


def start(): #開始関数
    GameScreen = app.Window(config.SCREEN_SIZE, "ブロック崩しv0.1")
    screen = GameScreen.screen
    time.sleep(0.5)
    player = app.GameObj() #インスタンス化　プレーヤーを作った
    # ゲームループ
    while True:
        screen.fill(config.color['black'])   # 画面を黒色で塗りつぶす
        pygame.display.update()  # 画面を更新

        # イベント処理
        for event in pygame.event.get():
            app.key(event, player) #キーボード処理
            if event.type == QUIT:  # 終了イベント
                pygame.quit()
                sys.exit()
                

if __name__ == "__main__":
    start()