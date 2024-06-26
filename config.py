
# ======== 見た目 ==========
SCREEN_SIZE = (1280, 720) # 画面サイズ
CenterScreen = SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2

# -------- 色 ----------
def color(key:str) -> tuple[int, int, int]:
    '''
    color(色の名前)
    例
    >>> print(color('white'))
    (241, 248, 232)
    
    red
    green
    blue
    white
    black
    
    展望
    英語でなくても良いようにする
    '''
    result:dict[str, tuple[int, int, int]] ={ 
                    'red': (250, 112, 112),
                    'green': (95, 235, 182),
                    'blue': (66, 132, 227),
                    'white': (241, 248, 232), 
                    'black': (53, 55, 75),
                }
    return result[key]


fonts:list[str] = [ 'font/FGUIGENBOLD_0.otf',
                    'font/03スマートフォントUI_0.otf',
                    ]

images:dict[str, str] = {   'icon': 'image/icon.png',
                            'player': 'image/player.png',
                            'carsol': 'image/carsol.png',
                            'boll': 'image/boll.png'

                        }

# ====== 物理 =========
bollvyo = 5
g = 1
PLAYER_A = 5