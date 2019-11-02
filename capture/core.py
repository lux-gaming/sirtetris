from PIL import Image


class Capture:
    source_type = 'image'
    source = None
    game = None

    def capture(self):
        if self.source_type == 'image':
            self.from_image()

    def from_image(self):
        image = Image.open(self.source)

    def set_source(self, reference):
        self.source = reference
