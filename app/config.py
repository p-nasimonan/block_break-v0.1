'''
設定ファイル

'''
import os

FPS = 60
dt = 60/FPS
delta_time = dt

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
                            'boll': 'image/boll.png',
                            'block1': 'image/block1.png',
                            'block2': 'image/block2.png',
                        }

# ====== 物理 =========
bollvyo = -8
bollvxo = 5
g = 1
PLAYER_A = 5

# ===== ブロックの設定 =========

block_sizex = 50
block_sizey = 50
spacex = 20
spacey = 5
blockpos =  [
        "1111111111",
        "1000000001",
        "1011111101",
        "1000000001",
        "1111111111",
        "0000000000"  
    ]

# ======= ステージの設定 =========
stage_list = [
    blockpos,
    blockpos,
    blockpos,
    blockpos,
    blockpos,
]
STAGE_FILE = ['stage/stage0.txt', 'stage/stage1.txt', 'stage/stage2.txt', 'stage/stage3.txt', 'stage/stage4.txt', 'stage/stage5.txt']
def write_default_stage(stage):
    print(f'ステージファイルが存在しないので {STAGE_FILE[stage]} を作成します')
    default_pattern = [
        "1111111111",
        "1000000001",
        "1011111101",
        "1000000001",
        "1111111111",
        "0000000000"  
    ]
    with open(STAGE_FILE[stage], 'w') as file:
        for line in default_pattern:
            file.write(line + "\n")

def open_stage(stage):
    if not os.path.exists(STAGE_FILE[stage]):
        write_default_stage(stage)

    with open(STAGE_FILE[stage], 'r') as file:
        return file.read().splitlines()

# --- 直感的なリストから座標に変換 ----
def blocklist_convert(blocklist:list[int]) -> tuple[list[tuple[int, int]], list[str]]:
    result_xy = []
    result_img = []
    reference_x = CenterScreen[0] - ((block_sizex + spacex) * len(blocklist[0]) // 2)

    for y, line in enumerate(blocklist):
        for x, char in enumerate(line):
            if char == "1":
                result_xy.append(((block_sizex+spacex)*x + reference_x, (block_sizey+spacey)*y))
                result_img.append(images['block1'])
            elif char == "0":
                continue
            else:
                raise ValueError(f'blocklist[{y}][{x}]は無効な値です: {char}')
    return result_xy, result_img
