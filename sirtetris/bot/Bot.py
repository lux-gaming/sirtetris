from abc import abstractmethod
from sirtetris.controller.Controller import Command
from random import randint

from time import time


class Bot:
    gamestate = None

    @abstractmethod
    def play(self):
        pass

    def set_gamestate(self, gamestate):
        self.gamestate = gamestate


class RandomBot(Bot):
    last_command = 0

    def play(self):
        # Only one command per second
        if self.last_command + 0.5 > time():
            return []

        self.last_command = time()

        buttons = ['LEFT', 'RIGHT', 'DOWN']
        button = buttons[randint(0, len(buttons)-1)]

        commands = [
            Command(button, 'tap'),
        ]

        return commands
