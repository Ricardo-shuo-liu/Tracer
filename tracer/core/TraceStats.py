from dataclasses import dataclass
import time
from .Color import set_color

@dataclass
class FuncStat:
    call_count: int = 0
    total_cost: float = 0.0
    min_cost: float = float("inf")
    max_cost: float = 0.0

    def add_record(self,
                   cost: float):
        self.call_count += 1
        self.total_cost += cost
        if cost < self.min_cost:
            self.min_cost = cost
        if cost > self.max_cost:
            self.max_cost = cost

    @property
    def avg_cost(self) -> float:
        if self.call_count == 0:
            return 0.0
        return self.total_cost / self.call_count
    
class TraceStats:
    def __init__(self):
        self.data: dict[str, FuncStat] = {}
        self.running_start: dict[object, tuple[str, float]] = {}

    def reset(self):
        """Drop data from a previous traced run."""
        self.data.clear()
        self.running_start.clear()

    def enter_func(self, frame, func_name: str):
        start = time.perf_counter()
        self.running_start[frame] = (func_name, start)

    def exit_func(self, frame) -> tuple[str, float] | None:
        if frame not in self.running_start:
            return None
        func_name, start = self.running_start.pop(frame)
        cost = time.perf_counter() - start

        if func_name not in self.data:
            self.data[func_name] = FuncStat()
        self.data[func_name].add_record(cost)
        return func_name, cost

    def format_report(self,
                      setcolor:bool=False) -> str:
        title = "===== Function Trace Statistics Report ====="
        if setcolor:
            header = "".join([
                set_color(s=f"{'Function':<16}",color="blue"),
                set_color(s=f"{'Calls':<8}",color="blue"),
                set_color(s=f"{'Total(s)':<10}",color="blue"),
                set_color(s=f"{'Avg(s)':<10}",color="blue"),
                set_color(s=f"{'Min(s)':<10}",color="blue"),
                set_color(s=f"{'Max(s)':<10}",color="blue"),
            ])
            rows = []
            for name, stat in self.data.items():
                rows.append("".join([
                    set_color(s=f"{name:<16}",color='green'),
                    set_color(s=f"{stat.call_count:<8}",color="yellow"),
                    set_color(s=f"{stat.total_cost:<10.4f}",color="yellow"),
                    set_color(s=f"{stat.avg_cost:<10.4f}",color="yellow"),
                    set_color(s=f"{stat.min_cost:<10.4f}",color="yellow"),
                    set_color(s=f"{stat.max_cost:<10.4f}",color="yellow"),
                ]))
        else:
            header = f"{'Function':<16}{'Calls':<8}{'Total(s)':<10}{'Avg(s)':<10}{'Min(s)':<10}{'Max(s)':<10}"
            rows = [
                f"{name:<16}{stat.call_count:<8}{stat.total_cost:<10.4f}{stat.avg_cost:<10.4f}{stat.min_cost:<10.4f}{stat.max_cost:<10.4f}"
                for name, stat in self.data.items()
            ]
        return "\n".join(["", title, header, *rows, "=" * len(title), ""])

    def print_report(self,
                     setcolor:bool=False):
        print(self.format_report(setcolor=setcolor), end="")