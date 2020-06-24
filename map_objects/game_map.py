from map_objects.tile import Tile


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.init_tiles()

    def init_tiles(self):
        tiles = [[Tile(False) for y in range(self.height)]
                 for x in range(self.width)]

        # TODO magic numbers!
        tiles[20][12].blocked = True
        tiles[20][12].block_sight = True
        tiles[21][12].blocked = True
        tiles[21][12].block_sight = True
        tiles[22][12].blocked = True
        tiles[22][12].block_sight = True

        return tiles
