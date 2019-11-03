from abc import abstractmethod
from PIL import Image
import numpy


class Capture:
    source = None
    game = None

    xtiles = None
    ytiles = None

    @abstractmethod
    def is_spawn_field_empty(self):
        pass

    @abstractmethod
    def get_tiles(self, x, y, width, height):
        pass


class ImageCapture(Capture):
    tile_width = None
    tile_height = None
    field_offset_x = None
    field_offset_y = None
    next_mino_offset_x = None
    next_mino_offset_y = None
    image = None

    @abstractmethod
    def __init__(self):
        pass

    def set_dimensions(self, tiles, tile_dimension, field_offset, next_mino_offset):
        self.xtiles = tiles['x']
        self.ytiles = tiles['y']
        self.tile_width = tile_dimension['width']
        self.tile_height = tile_dimension['height']
        self.field_offset_x = field_offset['x']
        self.field_offset_y = field_offset['y']
        self.next_mino_offset_x = next_mino_offset['x']
        self.next_mino_offset_y = next_mino_offset['y']

    def set_source(self, reference):
        self.source = reference

    def __call__(self, *args, **kwargs):
        self.capture()

    def capture(self):
        image = Image.open(self.source)
        if not image:
            print('I can\'t see shit.')

        self.image = image

        # Get blocks
        field = self.get_tiles(0, 0, self.xtiles, self.ytiles)
        self.game.state.set_blocks(field)

        # Get next tetromino
        # Check if it is a square piece
        square = self.get_field(self.next_mino_offset_x + 4, self.next_mino_offset_y + 9, 3, 3, image)

        column1 = square[0][0] and square[1][0] and not square[2][0]
        column2 = square[0][1] and square[1][1] and not square[2][1]
        column3 = not (square[0][2] and square[1][2] and square[2][2])

        if column1 and column2 and column3:
            square = numpy.ones((2, 2), dtype=bool)
            self.game.state.set_next_mino(square)
            self.game.state.capturing_done()
            return

        mino = self.get_field(self.next_mino_offset_x, self.next_mino_offset_y, 3, 3, image)

        if mino[0, 2] and mino[1, 2] and mino[2, 2] and mino[0, 1] and mino[1, 1] and mino[2, 1]:
            line = numpy.zeros((4, 1), dtype=bool)
            line[0, 0] = line[1, 0] = line[2, 0] = line[3, 0] = True
            self.game.state.set_next_mino(line)
            self.game.state.capturing_done()
            return

        self.game.state.set_next_mino(mino)
        self.game.state.capturing_done()

    def is_spawn_field_empty(self):
        return self.get_tile(5, 0)

    def get_tiles(self, x, y, width, height):
        offset_x = self.field_offset_x + x*self.tile_width
        offset_y = self.field_offset_y + y*self.tile_height
        field = self.get_field(offset_x, offset_y, width, height, self.image)
        return field

    def get_tile(self, x, y):
        return self.get_tiles(x, y, 1, 1)

    def get_field(self, offset_x, offset_y, width, height, image):
        field = numpy.zeros((width, height), dtype=bool)
        for x in range(0, width):
            for y in range(0, height):
                x1 = offset_x + x * self.tile_width
                x2 = x1 + self.tile_width
                y1 = offset_y + y * self.tile_height
                y2 = y1 + self.tile_height

                tile = image.crop((x1, y1, x2, y2))
                # getbbox returns False if the box is completely black
                field[x, y] = tile.getbbox()

        return field
