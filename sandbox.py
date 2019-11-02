from capture.FceuxStreamCapture import FceuxStreamCapture
from gamestate.models import Game

capture = FceuxStreamCapture()

game = Game()
game.connect(capture)
game.capture.listen()
