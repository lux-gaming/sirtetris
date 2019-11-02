from .core import ImageCapture


class NesImageCapture(ImageCapture):
    def __init__(self, reference):
        tiles = {'x': 10, 'y': 20}
        tile_dimension = {'width': 7, 'height': 7}
        field_offset = {'x': 86, 'y': 25}
        next_mino_offset = {'x': 186, 'y': 88}

        self.set_source(reference)
        self.set_dimensions(tiles, tile_dimension, field_offset, next_mino_offset)
