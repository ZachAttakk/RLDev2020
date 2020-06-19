# This class handles sprite sheets
# This was taken from www.scriptefun.com/transcript-2-using
# sprite-sheets-and-drawing-the-background
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)
# https://www.pygame.org/wiki/Spritesheet
import pygame


class spritesheet(object):
    def __init__(self, filename, tile_size=None, tile_gap=0):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as message:
            print('Unable to load spritesheet image: %s' % filename)
            raise SystemExit(message)
        self.tile_size = tile_size
        self.tile_gap = tile_gap
        self.filename = filename
    # Load a specific image from a specific rectangle

    def image_at(self, rectangle, colorkey=None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    # Load a whole bunch of images and return them as a list

    def images_at(self, rects, colorkey=None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]
    # Load a whole strip of images

    def load_strip(self, rect, image_count, colorkey=None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

    def sprite_at(self, pos, size=None, gap=None, colorkey=None):
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
            _x_pix = pos[0]
        if pos[1] != 0:
            _y_pix = pos[1]*(self.tile_size+self.tile_gap)
        else:
            _y_pix = pos[1]
        # use image_at to load the tile and return
        return(self.image_at((_x_pix, _y_pix, self.tile_size, self.tile_size)))
