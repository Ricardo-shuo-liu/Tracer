import os

class FileWriter:
    def __init__(self, path, overwrite):
        # Accept str, bytes and os.PathLike paths (e.g. pathlib.Path).
        self.path = os.fsdecode(path)
        self.overwrite = overwrite
    def write(self, s):
        with open(self.path, 'w' if self.overwrite else 'a', encoding='utf-8') as output_file:
            output_file.write(s)
            self.overwrite = False