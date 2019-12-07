from datetime import datetime

class Debug:
    cli = False
    file = None

    def __init__(self, cli=False, file=None):
        self.cli = cli
        self.file = file

        if self.file is not None:
            self.file = open(file, 'w+')
            self('Opened debug file...')
            self('It is now ' + str(datetime.now()))

    def __call__(self, *args):
        if self.cli:
            for arg in args:
                print(arg)

        if self.file is not None:
            for arg in args:
                self.file.write(str(arg) + '\n')


class DebugMixin:
    debug = None

    def init_debug(self, cli, file):
        self.debug = Debug(cli=cli, file=file)
