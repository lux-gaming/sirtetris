class Debug:
    cli = False
    file = None

    def __init__(self, cli=False, file=None):
        self.cli = cli
        self.file = file

        if self.debug.file is not None:
            self.debug.file = open(file, 'w+')
            self.debug('Opened debug file...')

    def __call__(self, *args):
        if self.cli:
            for arg in args:
                print(arg)

        if self.file is not None:
            for arg in args:
                self.file.write(str(arg) + '\n')


class DebugMixin:
    debug = None

    def init(self, cli, file):
        self.debug = Debug(cli=cli, file=file)
