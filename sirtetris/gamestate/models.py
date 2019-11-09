import numpy

from sirtetris.capture.core import Capture
from sirtetris.controller.Controller import Controller, Command


class Game:
    state = None
    capture = None
    controller = None
    bot = None
    silent = None

    def __init__(self, silent=False):
        self.state = GameState()
        self.state.game = self
        self.silent = silent

    def connect(self, thing):
        from sirtetris.bot.Bot import Bot

        if isinstance(thing, Capture):
            self.capture = thing
            self.capture.game = self
            self.state.width = self.capture.xtiles
            self.state.height = self.capture.ytiles
            return self
        elif isinstance(thing, Controller):
            self.controller = thing
            return self
        elif isinstance(thing, Bot):
            self.bot = thing
            return self

        print('Error: Cannot determine the type of that thing.')

    def game_state_done(self):
        if not self.silent:
            print(self.state)

        self.state.track_live_mino()

        if self.controller and self.bot:
            self.bot.set_gamestate(self.state)
            commands = self.bot.play()
            for command in commands:
                self.controller.send(command)


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

    def track_live_mino(self, command=None):
        mino = self.live_mino
        mino_x = self.live_mino_x
        mino_y = self.live_mino_y

        # Check each rotation, begin with last known rotation
        rotations = [
            [mino, mino_x, mino_y],
            self.rotate_right(mino, mino_x, mino_y),
            self.rotate_right(self.rotate_right(mino, mino_x, mino_y), mino_x, mino_y),
            self.rotate_right(self.rotate_right(self.rotate_right(mino, mino_x, mino_y), mino_x, mino_y), mino_x, mino_y),
        ]

        for rotation in rotations:
            if rotation is None:
                continue

            mino, mino_x, mino_y = rotation

            # Speculate where it could be, begin with last known position
            speculations = [
                [0, 0],
                [0, 1],  # One down
                [1, 0],  # One right
                [1, 1],  # One right one down
                [-1, 0],  # One left
                [-1, 0],  # One left one down
            ]

            for speculation in speculations:
                sx = speculation[0]
                sy = speculation[1]

                print('Speculating')
                print(self.field_to_string(self.live_blocks, mino, mino_x + sx, mino_y + sy))

                # Check if live tetromino is there
                empty_field = numpy.zeros((self.width, self.height), bool)
                for x in range(len(mino)):
                    for y in range(len(mino)):
                        try:
                            empty_field = mino[mino_x + x + sx, mino_y + y + sy]
                        except Exception:
                            pass
                mino_present = numpy.isin(empty_field, self.live_blocks).all()
                print('MINO PRESENT?', mino_present)

                # If this seems like the live tetromino, update it and return True
                if mino_present:
                    print('Updating live mino on position', str(mino_x + sx), str(mino_y + sy))
                    print(self.field_to_string(mino))
                    self.live_mino = mino
                    self.live_mino_x = mino_x + sx
                    self.live_mino_y = mino_y + sy
                    return True

        # We have not found the live tetromino
        exit()
        return False

    def switch_live_mino(self):
        self.live_mino = self.next_mino
        self.live_mino_x = 3 if len(self.live_mino) == 4 else 4
        self.live_mino_y = 0

    def switch_frame(self):
        self.last_blocks = self.live_blocks
        self.live_blocks = numpy.zeros((self.width, self.height), dtype=bool)

    def capturing_done(self):
        self.next_mino = self.trim_field(self.next_mino)
        self.game.game_state_done()
        self.switch_frame()

    def set_block(self, x, y, color=None):
        self.live_blocks[x, y] = True

    def set_blocks(self, field):
        self.live_blocks = field

    def set_next_mino(self, field):
        field = self.trim_field(field)
        differences = self.next_mino != field
        if not isinstance(differences, bool):
            differences = differences.any()

        if differences:
            self.switch_live_mino()
            self.next_mino = field

    def set_next_mino_block(self, x, y, color=None):
        self.next_mino[x, y] = True

    def __str__(self):
        out = 'Field:\n\n'
        out += self.field_to_string(self.live_blocks)

        out += '\nNext tetromino:\n\n'
        out += self.field_to_string(self.next_mino)

        out += '\nLive tetromino (' + str(self.live_mino_x) + ',' + str(self.live_mino_y) + '):\n\n'
        out += self.field_to_string(self.live_mino)

        return out

    @staticmethod
    def field_to_string(field, mino=None, mino_x=0, mino_y=0):
        if field is None:
            return ''

        width = len(field)
        if width == 0:
            return ''

        result = '   0123456789\n'

        height = len(field[0])
        for y in range(height):
            result += str(y).rjust(2, ' ') + ' '
            for x in range(width):
                if field[x, y]:
                    result += 'X'
                else:
                    result += '.'

                if mino is not None and x >= mino_x and y >= mino_y:
                    offx = x - mino_x
                    offy = y - mino_y
                    if offx < len(mino) and offy < len(mino[0]):
                        if mino[offx, offy]:
                            nresult = list(result)
                            nresult[-1] = 'M'
                            result = "".join(nresult)

            result += '\n'

        result += '   0123456789'
        return result

    """
    Do I look like a mathematician? HELP.
    Write a test and then rewrite this mess.
    Ref: https://vignette.wikia.nocookie.net/tetrisconcept/images/3/3d/SRS-pieces.png/revision/latest?cb=20060626173148
    """
    def rotate_right(self, field, x, y):
        if field is None or len(field) == 0:
            return None

        oh = self.translate(['XX', 'XX'])
        if numpy.array_equal(oh, field):
            return [oh, x, y]

        line = self.translate(['XXXX'])
        if numpy.array_equal(line, field):
            return [self.translate(['X', 'X', 'X', 'X']), x+2, y-2]
        if numpy.array_equal(self.rot270(line), field):
            return [self.translate(['XXXX']), x-2, y+2]

        ess = self.translate([' XX', 'XX '])
        if numpy.array_equal(ess, field):
            return [self.translate(['X ', 'XX', ' X']), x+1, y-1]
        if numpy.array_equal(self.rot270(ess), field):
            return [self.translate([' XX', 'XX ']), x-1, y+1]

        zet = self.translate(['XX ', ' XX'])
        if numpy.array_equal(zet, field):
            return [self.translate([' X', 'XX', 'X ']), x+1, y-1]
        if numpy.array_equal(self.rot270(zet), field):
            return [self.translate(['XX ', ' XX']), x-1, y+1]

        ell = self.translate(['  X', 'XXX'])
        if numpy.array_equal(ell, field):
            return [self.translate(['X ', 'X ', 'XX']), x+1, y]
        if numpy.array_equal(self.rot270(ell), field):
            return [self.translate(['XXX', 'X  ']), x-1, y+1]
        if numpy.array_equal(self.rot270(self.rot270(ell)), field):
            return [self.translate(['XX', ' X', ' X']), x, y-1]
        if numpy.array_equal(numpy.rot90(ell), field):
            return [self.translate(['  X', 'XXX']), x, y-1]

        iot = self.translate(['X  ', 'XXX'])
        if numpy.array_equal(iot, field):
            return [self.translate(['XX', 'X ', 'X ']), x+1, y]
        if numpy.array_equal(self.rot270(iot), field):
            return [self.translate(['XXX', '  X']), x-1, y+1]
        if numpy.array_equal(self.rot270(self.rot270(iot)), field):
            return [self.translate([' X', ' X', 'XX']), x, y-1]
        if numpy.array_equal(numpy.rot90(iot), field):
            return [self.translate(['X  ', 'XXX']), x, y-1]

        teh = self.translate([' X ', 'XXX'])
        if numpy.array_equal(teh, field):
            return [self.translate([' X ', ' XX', ' X ']), x+1, y]
        if numpy.array_equal(self.rot270(teh), field):
            return [self.translate(['XXX', ' X ']), x-1, y+1]
        if numpy.array_equal(self.rot270(self.rot270(teh)), field):
            return [self.translate([' X', 'XX', ' X']), x, y-1]
        if numpy.array_equal(numpy.rot90(teh), field):
            return [self.translate([' X ', 'XXX']), x, y-1]

        return [[], 0, 0]

    @staticmethod
    def rot270(field):
        return numpy.rot90(numpy.rot90(numpy.rot90(field)))

    def rotate_left(self, field, x, y):
        return [self.rotate_right(self.rotate_right(self.rotate_right(field))), x, y]

    @staticmethod
    def trim_field(field):
        width = len(field)
        if width == 0:
            return []

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

    @staticmethod
    def translate(string):
        description = string
        tetromino = numpy.zeros((len(description[0]), len(description)), dtype=bool)
        for x in range(len(description[0])):
            for y in range(len(description)):
                tetromino[x, y] = description[y][x] == 'X'

        return tetromino
