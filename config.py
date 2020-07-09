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
        "grey": (100, 100, 100),
        "player": (207, 198, 184),
        "blue": (60, 172, 215),
        "yellow": (244, 180, 27),
        "floor": (70, 45, 60),
        "player_atk": (0xE0, 0xE0, 0xE0),
        "enemy_atk": (0xFF, 0xC0, 0xC0),
        "player_die": (0xFF, 0x30, 0x30),
        "enemy_die": (0xFF, 0xA0, 0x30),
        "welcome_text": (0x20, 0xA0, 0xFF),
        "bar_text": "white",
        "bar_filled": (0x0, 0x60, 0x0),
        "bar_empty": (0x40, 0x10, 0x10)
    }

    @classmethod
    def get_colour(cls, col_name: str):
        """Get colour by name. It's possible to set a colour to another colour."""
        # Clear history list
        previous = []
        result = col_name

        # First check for recursion
        while isinstance(result, str):
            result = cls.Colours.get(result)
            # Only recurse if we haven't seen this colour name before
            if result in previous:
                return None
            else:
                previous.append(result)

        return result
    Fonts = {
        "block": {"path": os.path.join("assets", "Kenney Blocks.ttf")},
        "minisq": {"path": os.path.join("assets", "Kenney Mini Square.ttf")},
        "mini": {"path": os.path.join("assets", "Kenney Mini.ttf")}
    }
    SpriteSheets = {
        "1bit": {
            "path": os.path.join("assets", "monochrome_transparent.png"),
            "tile_size": 16,
            "tile_gap": 1
        }
    }
    Sprites = {
        "player": {
            "values": (30, 9),
            "sheet": "1bit",
            "fgcolour": "player"
        },
        "blue": {
            "values": (18, 7),
            "sheet": "1bit",
            "fgcolour": "blue"
        },
        "yellow": {
            "values": (18, 8),
            "sheet": "1bit",
            "fgcolour": "yellow"
        },
        "floor": {
            "values": (0, 0),
            "sheet": "1bit",
            "bgcolour": "floor"
        },
        "wall": {
            "values": (10, 17),
            "sheet": "1bit",
            "bgcolour": "floor"
        }
    }
    Game = {
        "map_width": 25,
        "map_height": 18,
        "room_size_max": 6,
        "room_size_min": 3,
        "rooms_max": 10,
        "fov_radius": 4,
        "monsters_per_room": 2
    }
    Display = {
        "fullscreen": False,
        "game_height": 300,
        "game_width": 400,
        "tile_size": 16,
        "scanline_opacity": 20,
        "scanline_spacing": 3,
        "darkness_opacity": 220
    }
