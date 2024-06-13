import world
import app
import config
import window

import pygame
from pygame.locals import *
import sys
import time


def start(): #開始関数
    screen = window.init(config.SCREEN_SIZE, "ブロック崩しv0.1")
    time.sleep(0.5)
    
    # ゲームループ
    while True:
        screen.fill((0,0,255))   # 画面を青色で塗りつぶす
        pygame.display.update()  # 画面を更新

        # イベント処理
        for event in pygame.event.get():
            app.key(event, app.gameobj()) #キーボード処理
            if event.type == QUIT:  # 終了イベント
                pygame.quit()
                sys.exit()
                

if __name__ == "__main__":
    start()