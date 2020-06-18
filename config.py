'''Configuration class. Eventually this will load a JSON file on startup'''
from enum import Enum


class Colors(Enum):
    '''Color presets (R,G,B)'''
    black = (0, 0, 0)
    white = (255, 255, 255)
    grey = (100, 100, 100)


class Sprites(Enum):
    '''Strings for sprite files'''
    player = "tile_0004.png"


class Game(Enum):
    '''Game Settings'''
    fullscreen = False
    game_height = 300
    game_width = 400
    scale = 2.0
    tile_size = 8
