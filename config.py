'''Configuration class. Eventually this will load a JSON file on startup'''
import os
import json
from enum import Enum


class Config:
    """Configuration class that loads everything from config.json"""
    Colours = {
        "empty": (0, 0, 0, 0),
        "black": (0, 0, 0),
        "white": (255, 255, 255),
        "grey": (100, 100, 100)
    }
    SpriteSheets = {
        "1bit": {
            "path": os.path.join("tiles", "monochrome_transparent.png"),
            "tile_size": 16,
            "tile_gap": 1
        }
    }
    Sprites = {
        "player": {
            "values": (30, 9),
            "sheet": "1bit",
            "fgcolour": (207, 198, 184)
        },
        "blue": {
            "values": (18, 7),
            "sheet": "1bit",
            "fgcolour": (60, 172, 215)
        },
        "yellow": {
            "values": (18, 8),
            "sheet": "1bit",
            "fgcolour": (244, 180, 27)
        },
        "floor": {
            "values": (0, 0),
            "sheet": "1bit",
            "bgcolour": (70, 45, 60)
        },
        "wall": {
            "values": (10, 17),
            "sheet": "1bit",
            "bgcolour": (70, 45, 60)
        }
    }
    Game = {
        "map_width": 25,
        "map_height": 20,
        "room_size_max": 6,
        "room_size_min": 3,
        "rooms_max": 10,
        "fov_radius": 4,
        "monsters_per_room": 2
    }
    Display = {
        "fullscreen": False,
        "game_height": 320,
        "game_width": 400,
        "scale": 1.0,
        "tile_size": 16,
        "scanline_opacity": 20,
        "scanline_spacing": 3,
        "darkness_opacity": 220
    }
