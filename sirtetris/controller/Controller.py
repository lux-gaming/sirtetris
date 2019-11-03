from abc import abstractmethod


class Command:
    button = None
    action = None

    def __init__(self, button='A', action='tap'):
        self.button = button
        self.action = action


class Controller:
    @abstractmethod
    def send(self, command):
        pass



