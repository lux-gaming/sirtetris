from .Controller import Command, Controller
import keyboard

from gi.repository import Gdk
from time import sleep

import gi
gi.require_version('Gtk', '3.0')


class WindowController(Controller):

    def send(self, command):
        # Only send commands if Fceux window is active
        window = Gdk.get_default_root_window()
        screen = window.get_screen()
        w = screen.get_active_window()
        if not w.get_geometry().width == 288:
            return

        keys = {
            'A': 'f',
            'B': 'd',
            'UP': 'up',
            'DOWN': 'down',
            'LEFT': 'left',
            'RIGHT': 'right',
        }

        key = keys[command.button]

        print(command.action, command.button, key)

        if command.action == 'press':
            keyboard.press(key)
        elif command.action == 'release':
            keyboard.release(key)
        elif command.action == 'tap':
            keyboard.press(key)
            sleep(0.05)
            keyboard.release(key)
