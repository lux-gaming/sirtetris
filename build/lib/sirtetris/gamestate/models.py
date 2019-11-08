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

        if self.controller and self.bot:
            self.bot.set_gamestate(self.state)
            commands = self.bot.play()
            for command in commands:
                self.controller.send(command)
                self.state.track_live_mino(command)

        self.state.track_live_mino()


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
        mino_width = len(self.live_mino)
        if mino_width == 0:
            return

        # Check if mino can move where it is commanded to move (f=a=clockwise)
        if command and self.live_mino is not None:
            mino = self.live_mino
            mino_x = self.live_mino_x
            mino_y = self.live_mino_y

            if command.button == 'A':
                mino = self.rotate_right(mino)
            elif command.button == 'B':
                mino = self.rotate_left(mino)
            elif command.button == 'LEFT':
                mino_x -= 1
            elif command.button == 'RIGHT':
                mino_x += 1
            elif command.button == 'DOWN':
                mino_y += 1

            mino_width = len(mino)
            mino_height = len(mino[0])

            tiles = self.game.capture.get_tiles(mino_x, mino_y, mino_width, mino_height)
            can_fit = True
            for x in range(mino_width):
                for y in range(mino_height):
                    if mino[x, y] and tiles[x, y]:
                        can_fit = False

            if can_fit:
                print('Command', command.button, 'can fit', can_fit)
                self.live_mino_x = mino_x
                self.live_mino_y = mino_y
                self.live_mino = mino

        # Check if the mino is still where we think it is
        mino_width = len(self.live_mino)
        mino_height = len(self.live_mino[0])
        mino_field = self.game.capture.get_tiles(self.live_mino_x, self.live_mino_y, mino_width, mino_height)
        mino_present = ((mino_field + self.live_mino) == self.live_mino).all()

        # If it's not present, look a few tiles further down
        look_further = 1
        while not mino_present and look_further < 5:
            mino_field = self.game.capture.get_tiles(
                self.live_mino_x, self.live_mino_y+look_further,
                mino_width, mino_height
            )

            mino_present = ((mino_field + self.live_mino) == self.live_mino).all()

            if mino_present:
                self.live_mino_y += 1
            else:
                look_further += 1

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
                    result += ' '
            result += '\n'

        result += '   0123456789'
        return result

    @staticmethod
    def rotate_right(field):
        return numpy.rot90(numpy.rot90(numpy.rot90(field)))

    @staticmethod
    def rotate_left(field):
        return numpy.rot90(field)

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
