import pygame
SCREEN_SIZE = (1280, 720) # 画面サイズ
CenterScreen = SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2
color:dict[str, tuple] ={  'red': (250, 112, 112),
                'green': (95, 235, 182),
                'blue': (66, 132, 227),
                'white': (241, 248, 232), 
                'black': (53, 55, 75),
            }

fonts:list[str] = [  'font/FGUIGENBOLD_0.otf',
                'font/03スマートフォントUI_0.otf',
            ]

images:dict[str] = { 'icon': 'image/icon.png',
                'player': 'image/cloud.png',
                'carsol': 'image/carsol.png',

}
