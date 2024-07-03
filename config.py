
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
bollvyo = 5
bollvxo = 5
g = 1
PLAYER_A = 5

# ===== ブロックの設定 =========
block_sizex = 100
block_sizey = 100
space = 10
blockpos =  [
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]

block_img_path = [images['block1'], images['block2']]

# --- 直感的なリストから座標に変換 ----
def blocklist_convert(blocklist:list[list[int]]) -> tuple[list[tuple[int, int]], list[str]]:
    result_xy = []
    result_img = []
    for i in range(len(blocklist)):
        for j in range(len(blocklist[i])):
            if blocklist[i][j] == 1:
                result_xy.append(((block_sizex+space)*i, (block_sizey+space)*j))
                result_img.append(block_img_path[0])
            elif blocklist[i][j] == 0:
                continue
            else:
                raise ValueError(f'blocklist[{i}][{j}]は無効な値です: {blocklist[i][j]}')
    return result_xy, result_img

block_xy, block_imgs = blocklist_convert(blockpos)