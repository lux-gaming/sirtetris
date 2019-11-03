from .core import ImageCapture


class NesImageCapture(ImageCapture):
    def __init__(self, reference):
        tiles = {'x': 10, 'y': 20}
        tile_dimension = {'width': 8, 'height': 8}
        field_offset = {'x': 85, 'y': 24}
        next_mino_offset = {'x': 186, 'y': 88}

        self.set_source(reference)
        self.set_dimensions(tiles, tile_dimension, field_offset, next_mino_offset)
