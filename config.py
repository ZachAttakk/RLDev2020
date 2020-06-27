'''Configuration class. Eventually this will load a JSON file on startup'''
import os
import json
from enum import Enum


class Config:
    """Configuration class that loads everything from config.json"""

    def __init__(self):

        # create defaults
        self.Colors = {
            "empty": (0, 0, 0, 0),
            "black": (0, 0, 0),
            "white": (255, 255, 255),
            "grey": (100, 100, 100)
        }
        self.SpriteSheets = {
            "base":
            {
                "path": os.path.join("tiles", "roguelikeSheet_transparent.png"),
                "tile_size": 16,
                "tile_gap": 1
            },
            "char": {
                "path": os.path.join("tiles", "roguelikeChar_transparent.png"),
                "tile_size": 16,
                "tile_gap": 1
            }
        }
        self.Sprites = {
            "player": {
                "values": (0, 6),
                "sheet": "char"
            },
            "npc": {
                "values": (0, 11),
                "sheet": "char"
            },
            "floor": {
                "values": (6, 2),
                "sheet": "base"
            },
            "wall": {
                "values": (18, 15),
                "sheet": "base"
            }
        }
        self.Game = {
            "fullscreen": False,
            "game_height": 320,
            "game_width": 400,
            "scale": 2.0,
            "tile_size": 16,
            "map_width": 25,
            "map_height": 20
        }

        # grab settings file
        try:
            with open("config.json", "r") as file:
                settings = json.load(file)
                if len(settings) > 0:
                    self.__load_config(settings)
        except FileNotFoundError as error:
            print(error)
        except json.JSONDecodeError as error:
            print("error")

    def __load_config(self, obj):
        for entry in obj:
            if entry == "Colors":
                for _col in obj["Colors"]:
                    # Classic key: value pair
                    self.Colors[_col["name"]] = tuple(_col["values"])
            if entry == "SpriteSheets":
                for _sht in obj["SpriteSheets"]:
                    # ID by name
                    # path is file path
                    # tile_size is the pixels across (must be square)
                    # tile_gap is the number of pixels between tiles (default 0)
                    self.SpriteSheets[_sht["name"]] = {
                        "path": os.path.join("tiles", _sht["path"]),
                        "tile_size": _sht.get("tile_size") or 16,
                        "tile_gap": _sht.get("tile_gap") or 0
                    }
            if entry == "Sprites":
                for _spr in obj["Sprites"]:
                    # ID by name
                    # sheet is the name of the sheet on which this sprite lives
                    # values is (x,y) in tiles
                    self.Sprites[str(_spr["name"])] = {
                        "values": tuple(_spr["values"]),
                        "sheet": _spr["sheet"]
                    }
            if entry == "Game":
                for _set in obj["Game"]:
                    # Classic key: value pair
                    self.Game[str(_set["name"])] = _set["value"]
