# TraceContext.py
import sys

from .TraceStats import TraceStats
from tracer.exceptions.TraceError import TraceErrors

class TraceContext:
    def __init__(self,
                 workflow,
                 time_trace:bool=False,
                 set_color:bool=False,
                 exception_trace:bool=False,
                 show_locals:bool=False,
                 exception_json_path:str|None=None):
        self.prefix = ""
        self.workflow = workflow
        self.time_trace = time_trace
        self.set_color = set_color
        self.output_content = []
        self.stats = TraceStats() if time_trace else None

        self.exception_trace = exception_trace
        self.show_locals = show_locals
        self.exception_json_path = exception_json_path
        self.errors = TraceErrors(show_locals=show_locals) if exception_trace else None
        # frame -> ExcRecord : exception raised in that frame, not yet resolved
        self.pending_exc: dict = {}

    def begin_run(self):
        """Reset per-run state so reports describe only the latest run."""
        self.prefix = ""
        self.output_content.clear()
        self.pending_exc.clear()
        if self.stats is not None:
            self.stats.reset()
        if self.errors is not None:
            self.errors.reset()

    def indent(self):
        self.prefix += "|  "

    def dedent(self):
        if len(self.prefix) >= 3:
            self.prefix = self.prefix[:-3]
    def add(self,output_line):
        self.output_content.append(output_line)    
    def outputcontrol(self):
        if not self.output_content:
            return
        s = "\n".join(self.output_content) + "\n"
        self.output_content.clear()
        self._emit(s)

    def _emit(self, s):
        """Write to every target without letting a failing target mask the
        exception that may be propagating out of the traced scope."""
        try:
            self.workflow.forward(s)
        except Exception as exc:
            print(f"tracer: failed to write output: {exc}", file=sys.stderr)

    def finish(self):
        """Flush buffered trace output, then emit exception/time reports."""
        self.outputcontrol()
        if self.exception_trace and self.errors is not None:
            self.errors.finalize()
            self._emit(
                self.errors.format_report(setcolor=self.set_color)
            )
            if self.exception_json_path:
                try:
                    self.errors.export_json(self.exception_json_path)
                except Exception as exc:
                    print(
                        f"tracer: failed to write exception JSON: {exc}",
                        file=sys.stderr,
                    )
        if self.time_trace and self.stats is not None:
            self._emit(
                self.stats.format_report(setcolor=self.set_color)
            )
