from sirtetris.capture.FceuxStreamCapture import FceuxStreamCapture
from sirtetris.gamestate.models import Game

capture = FceuxStreamCapture()

game = Game()
game.connect(capture)
game.capture.listen()
