from dataclasses import dataclass
import time

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

    def print_report(self):
        print("\n===== Function Trace Statistics Report =====")
        print(f"{'Function':<16}{'Calls':<8}{'Total(s)':<10}{'Avg(s)':<10}{'Min(s)':<10}{'Max(s)':<10}")
        for name, stat in self.data.items():
            print(f"{name:<16}{stat.call_count:<8}{stat.total_cost:<10.4f}{stat.avg_cost:<10.4f}{stat.min_cost:<10.4f}{stat.max_cost:<10.4f}")
        print("============================================\n")