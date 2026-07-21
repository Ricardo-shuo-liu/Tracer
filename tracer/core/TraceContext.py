# TraceContext.py
class TraceContext:
    def __init__(self):
        self.prefix = ""

    def indent(self):
        self.prefix += "|  "

    def dedent(self):
        if len(self.prefix) >= 3:
            self.prefix = self.prefix[:-3]
