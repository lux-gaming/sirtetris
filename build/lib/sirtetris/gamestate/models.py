import numpy

from sirtetris.capture import Capture


class Game:
    state = None
    capture = None
    controller = None

    def __init__(self):
        self.state = GameState()
        self.state.game = self

    def connect(self, thing):
        if isinstance(thing, Capture):
            self.capture = thing
            self.capture.game = self
            self.state.width = self.capture.xtiles
            self.state.height = self.capture.ytiles
            return

        print('Error: Cannot determine type of that thing.')

    def game_state_done(self):
        print(self.state)


class GameState:
    game = None

    width = None
    height = None

    last_blocks = None
    live_blocks = None
    live_mino = numpy.zeros((3, 4), dtype=bool)
    live_mino_x = 0
    live_mino_y = 0
    next_mino = numpy.zeros((3, 4), dtype=bool)

    def switch_live_mino(self):
        self.live_mino = self.next_mino
        self.live_mino_x = 3 if len(self.live_mino) == 4 else 4
        self.live_mino_y = 0

    def switch_frame(self):
        self.last_blocks = self.live_blocks
        self.live_blocks = numpy.zeros((self.width, self.height), dtype=bool)

    def capturing_done(self):
        self.next_mino = self.trim_field(self.next_mino)

        # Check if we get hands on the next mino
        field_changed = self.last_blocks != self.live_blocks
        print(field_changed)
        mino_spawned = self.game.capture.is_spawn_field_empty()
        if field_changed.any() and mino_spawned:
            self.switch_live_mino()

        self.game.game_state_done()
        self.switch_frame()

    def set_block(self, x, y, color=None):
        self.live_blocks[x, y] = True

    def set_blocks(self, field):
        self.live_blocks = field

    def set_next_mino(self, field):
        self.next_mino = field

    def set_next_mino_block(self, x, y, color=None):
        self.next_mino[x, y] = True

    def __str__(self):
        out = 'Field:\n\n'
        for y in range(0, self.height):
            for x in range(0, self.width):
                out += 'X' if self.live_blocks[x, y] else '.'
            out += '\n'

        out += '\nNext tetromino:\n\n'
        if len(self.next_mino) > 0 and len(self.next_mino[0]) > 0:
            for y in range(len(self.next_mino[0])):
                for x in range(len(self.next_mino)):
                    out += 'X' if self.next_mino[x, y] else '.'
                out += '\n'

        return out

    @staticmethod
    def trim_field(field):
        width = len(field)
        height = len(field[0])

        # X offset
        no_x = True
        off_x = 0
        for x in range(width):
            for y in range(height):
                if field[x, y]:
                    no_x = False
            if no_x:
                off_x += 1

        # Y offset
        no_y = True
        off_y = 0
        for y in range(height):
            for x in range(width):
                if field[x, y]:
                    no_y = False
            if no_y:
                off_y += 1

        # Maxima
        max_x = 0
        max_y = 0
        for x in range(width):
            for y in range(height):
                max_x = x if field[x, y] and x > max_x else max_x
                max_y = y if field[x, y] and y > max_y else max_y

        return field[off_x:max_x+1, off_y:max_y+1]
