from .NesImageCapture import NesImageCapture
from gi.repository import Gdk
from time import sleep

import gi
gi.require_version('Gtk', '3.0')


class FceuxStreamCapture(NesImageCapture):

    def __init__(self):
        super().__init__('tetris.png')

    def listen(self):
        while True:
            sleep(0.025)  # 40 Hz capturing should be enough.
            window = Gdk.get_default_root_window()
            screen = window.get_screen()
            for i, w in enumerate(screen.get_window_stack()):
                if w.get_geometry().width == 288:
                    pb = Gdk.pixbuf_get_from_window(w, *w.get_geometry())
                    pb.savev("tetris.png", "png", (), ())
                    break

            self.capture()
