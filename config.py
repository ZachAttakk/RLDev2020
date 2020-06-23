'''Configuration class. Eventually this will load a JSON file on startup'''
import os
import json
from enum import Enum


class Config:
    """Configuration class that loads everything from config.json"""

    def __init__(self):

        # create defaults
        self.Colors = {
            "black": (0, 0, 0),
            "white": (255, 255, 255),
            "grey": (100, 100, 100)
        }
        self.SpriteSheets = {
            "base": os.path.join("tiles", "roguelikeSheet_transparent.png"),
            "char": os.path.join("tiles", "roguelikeChar_transparent.png")
        }
        self.Sprites = {
            "player": (0, 6),
            "npc": (0, 11)
        }
        self.Game = {
            "fullscreen": False,
            "game_height": 320,
            "game_width": 400,
            "scale": 2.0,
            "tile_size": 16,
            "tile_gap": 1
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
                    self.Colors[_col["name"]] = tuple(_col["values"])
            if entry == "SpriteSheets":
                for _sht in obj["SpriteSheets"]:
                    self.SpriteSheets[_sht["name"]] = str(
                        os.path.join("tiles", _sht["value"]))
            if entry == "Sprites":
                for _spr in obj["Sprites"]:
                    self.Sprites[str(_spr["name"])] = tuple(_spr["values"])
            if entry == "Game":
                for _set in obj["Game"]:
                    self.Game[str(_set["name"])] = _set["value"]
