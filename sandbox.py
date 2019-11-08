from sirtetris.gamestate.models import Game
from sirtetris.capture.FceuxStreamCapture import FceuxStreamCapture
from sirtetris.controller.WindowController import WindowController
from sirtetris.bot.Bot import RandomBot

capture = FceuxStreamCapture()
controller = WindowController()
bot = RandomBot()

game = Game()
game.connect(capture)
game.connect(controller)
game.connect(bot)
game.capture.listen()
