# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys


def init(size:tuple[int,int]=(480, 360), title:str="タイトル未定"):
    # Pygameを初期化
    pygame.init()
    # タイトルバーの文字列をセット
    pygame.display.set_caption(title)

    # SCREEN_SIZEの画面を作成
    return pygame.display.set_mode(size)

