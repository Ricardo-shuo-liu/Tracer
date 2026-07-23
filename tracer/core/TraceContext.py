# TraceContext.py
from .TraceStats import TraceStats

class TraceContext:
    def __init__(self,
                 logger,
                 time_trace:bool=False,
                 set_color:bool=False):
        self.prefix = ""
        self.logger = logger
        self.time_trace = time_trace
        self.set_color = set_color
        self.output_content = []
        self.stats = TraceStats() if time_trace else None
    def indent(self):
        self.prefix += "|  "

    def dedent(self):
        if len(self.prefix) >= 3:
            self.prefix = self.prefix[:-3]
    def add(self,output_line):
        self.output_content.append(output_line)    
    def outputcontrol(self):
        for line in self.output_content:
            print(line)
            if self.logger is not None:
                self.logger.info(line)
        self.output_content.clear()