# This class handles sprite sheets
# This was taken from www.scriptefun.com/transcript-2-using
# sprite-sheets-and-drawing-the-background
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)
# https://www.pygame.org/wiki/Spritesheet
# Heavily modified by me
# Sheets now remember their tile size and can provide sprites based on it
import pygame
from config import Config as CONFIG


def get_sheets(sheets):
    """Change a dictionary list of spritesheet info into a dictionary list of spritesheet objects

    Args:
        sheets (dict): Dictionary from config spritesheets

    Returns:
        dict: spritesheet objects
    """
    loaded_sheets = {}
    for i in sheets:
        # for each sheet in the list, grab the dictionary under it
        _sh = sheets.get(i)
        # make a spritesheet from it, add it to the dictionary that's being returned
        loaded_sheets[i] = Spritesheet(
            _sh.get("path"), _sh.get("tile_size"), _sh.get("tile_gap"))
        # and send them back
    return loaded_sheets


class Spritesheet(object):

    empty = pygame.Color(0, 0, 0, 0)
    darkened = pygame.Color(0, 0, 0, 200)

    def __init__(self, filename, tile_size=None, tile_gap=0):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as message:
            print('Unable to load spritesheet image: %s' % filename)
            raise SystemExit(message)
        self.tile_size = tile_size
        self.tile_gap = tile_gap
        self.filename = filename
    # Load a specific image from a specific rectangle

    def image_at(self, rectangle):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert_alpha()
        image.fill(self.empty)
        image.blit(self.sheet, (0, 0), rect)
    #    if colorkey is not None:
    #        if colorkey == -1:
    #            colorkey = image.get_at((0, 0))
    #        image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    # Load a whole bunch of images and return them as a list

    def images_at(self, rects):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect) for rect in rects]
    # Load a whole strip of images

    def load_strip(self, rect, image_count):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups)

    def sprite_at(self, pos, fgcolour=None, bgcolour=None, size=None, gap=None, ):
        "Loads sprite at position for the size of tile and gap between tiles provided"

        # Sanity check the size and gap
        if (size is None and self.tile_size is None):
            raise SystemError("Spritesheet has no size: %s" % self.filename)

        # set spritesheet values if provided
        # Theoretically this should always be the same once set
        if size is not None:
            self.tile_size = size
        if gap is not None:
            self.tile_gap = gap

        # calculate pixel positions
        if pos[0] != 0:
            _x_pix = pos[0]*(self.tile_size+self.tile_gap)
        else:
            _x_pix = 0
        if pos[1] != 0:
            _y_pix = pos[1]*(self.tile_size+self.tile_gap)
        else:
            _y_pix = 0

        # Make blank sprite of right size
        sprite = pygame.Surface(
            (self.tile_size, self.tile_size)).convert_alpha()
        sprite.fill(self.empty)

        # blit sprite onto blank surface
        sprite.blit(self.image_at((_x_pix, _y_pix,
                                   self.tile_size, self.tile_size)), (0, 0))

        # apply foreground colour if provided
        if fgcolour:
            _fg = pygame.Surface(
                (self.tile_size, self.tile_size)).convert_alpha()
            if isinstance(fgcolour, str):
                _fgcol = CONFIG.Colours.get(fgcolour)
            else:
                _fgcol = pygame.Color(*fgcolour)
            _fg.fill(_fgcol)
            # This superimposes the colour on top of the sprite
            sprite.blit(_fg, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # apply background if provided
        if bgcolour:
            _bg = pygame.Surface(
                (self.tile_size, self.tile_size)).convert_alpha()
            if isinstance(bgcolour, str):
                _bgcol = CONFIG.Colours.get(fgcolour)
            else:
                _bgcol = pygame.Color(*bgcolour)
            _bg.fill(_bgcol)
            # This superimposes the sprite on top of the background colour
            _bg.blit(sprite, (0, 0))
            return _bg
        else:
            # return the sprite without background colours
            return sprite
