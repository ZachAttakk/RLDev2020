'''Configuration class. Eventually this will load a JSON file on startup'''
import os
from enum import Enum


class Colors(Enum):
    '''Color presets (R,G,B)'''
    black = (0, 0, 0)
    white = (255, 255, 255)
    grey = (100, 100, 100)


class SpriteSheets(Enum):
    '''List of spritesheet addresses'''
    base = os.path.join("tiles", "roguelikeSheet_transparent.png")


class Sprites(Enum):
    '''Strings for sprite files'''
    player = (15, 5)


class Game(Enum):
    '''Game Settings'''
    fullscreen = False  # should the game start in fullscreen?
    game_height = 300  # widown width in pixels
    game_width = 400  # window size in pixels
    scale = 2.0  # scale of main map (not yet implemented)
    tile_size = 16  # size of tiles in pixels
    tile_gap = 1  # space between tiles in pixels
