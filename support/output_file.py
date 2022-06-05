import os


class OutputFile:
    def __init__(self, p):
        self.path = p
        if os.path.exists(p) and os.path.isfile(p):
            os.remove(p)
        self.file = open(self.path, "a")

    def get_file_size(self) -> int:
        return os.path.getsize(self.path)

    def write(self, element: str):
        self.file.write(element + '\n')

    def close(self):
        self.file.close()
