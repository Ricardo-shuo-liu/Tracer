# TraceContext.py


class TraceContext:
    def __init__(self,logger):
        self.prefix = ""
        self.logger = logger
    def indent(self):
        self.prefix += "|  "

    def dedent(self):
        if len(self.prefix) >= 3:
            self.prefix = self.prefix[:-3]
    
    def outputcontrol(
            self,
            line:str|None):
        print(line)
        if self.logger is not None:
            self.logger.info(line)