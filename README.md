# sirtetris

sirtetris is an engine for Tetris bots. Its core is the gamestate module which is engageable with the following things:

  * **capture**:
    * Sets the size of the game field (number of horizontal and vertical tiles), size of the tiles, where to find the next tetromino (piece),
    * analyze a source (e.g. an image) to provide methods to check whether a tile is occupied or not, whether the spawn field is occupied or not, and to get the tiles within a given dimension, and
    * sets the next tetromino.
  * **controller**:
    * Defines the command button (A, B, LEFT, RIGHT, UP, DOWN) and action (tap, press, release), and
    * provides a method to send the command to something (e.g. an emulator or a piece of hardware connected to a console).
  * **bot**:
    * Receives the gamestate and can return commands to the game.

The overall game loop is as follows:

 * The connected capturing method updates the game with a gamestate model,
 * the game invokes the connected bot with the gamestate,
 * the bot has arbitrary intelligence to decide which commands to return to the game,
 * the game sends those commands to the connected controller,
 * the controller executes the commands on its destination (emulator, console, ...).

## Getting started

The package comes with a ``sandbox.py`` which connects to a Fceux emulator for capturing and controlling, and lets a bot yield random commands:

``` python
from sirtetris.gamestate.models import Game
from sirtetris.capture.FceuxStreamCapture import FceuxStreamCapture
from sirtetris.controller.WindowController import WindowController
from sirtetris.bot.Bot import RandomBot

capture = FceuxStreamCapture()
controller = WindowController()
bot = RandomBot()

game = Game(silent=True)
game.connect(capture)
game.connect(controller)
game.connect(bot)
game.capture.listen()
```

To connect a custom bot simply create a class extending ``sirtetris.bot.Bot`` which returns a list of ``sirtetris.controller.Controller.Command``s.

Note: The controller ``sirtetris.controller.WindowController`` only works on Linux and needs to be executed as ``sudo`` to generate keyboard commands. Feel free to pull-request more controllers!

Note: ``sirtetris.capture.FceuxStreamCapture`` only works on Linux. Feel free to pull-request more capturing methods!

## License
```
Copyright (c) 2019 Sven Cannivy (sven.cannivy@gmail.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```