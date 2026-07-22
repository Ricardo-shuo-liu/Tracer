# TraceContext.py
from .TraceStats import TraceStats

class TraceContext:
    def __init__(self,logger,time_trace:bool=False):
        self.prefix = ""
        self.logger = logger
        self.time_trace = time_trace
        self.stats = TraceStats() if time_trace else None
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