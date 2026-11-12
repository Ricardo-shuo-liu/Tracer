# 耗时统计

通过 `time_trace=True` 启用：

```python
from tracer import tracer

@tracer(trace_entity=True, time_trace=True)
def fib(n):
    if n <= 1:
        return n
    return fib(n - 2) + fib(n - 1)

fib(3)
```

每条返回行会附带本次调用耗时：

```text
-> fib(n=3)
|  -> fib(n=1)
|  |  <- fib returned 1 | cost=0.000012s
...
```

追踪运行结束后输出汇总报告：

```text
===== Function Trace Statistics Report =====
Function        Calls   Total(s)  Avg(s)    Min(s)    Max(s)
fib             5       0.0002    0.0000    0.0000    0.0001
============================================
```

报告与追踪文本经过同一个 `output_way` 管道，因此可以写入文件、流或多个目标。

## 报告字段

| 列 | 含义 |
| --- | --- |
| `Function` | 函数名 |
| `Calls` | 本次运行中完成的调用次数 |
| `Total(s)` | 累计实际耗时 |
| `Avg(s)` | 平均调用耗时 |
| `Min(s)` / `Max(s)` | 最快与最慢调用 |

计时使用 `time.perf_counter()`，并以帧为键，因此递归调用会被分别统计。

## 统计范围

每次顶层运行开始时都会重置统计数据。被装饰函数调用三次会产生三份独立报告，每份只覆盖当次运行；重复使用同一个 `Tracer` 上下文管理器时同样如此。
