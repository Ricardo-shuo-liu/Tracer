# Tracer

**一个轻量级的 Python 函数调用侵入式追踪器。**

Tracer 可以记录指定函数的调用树、统计每个函数的耗时、提取异常及其完整传播路径，并让所有输出统一经过一条可配置的管道。它不依赖任何第三方运行时库。

```python
from tracer import tracer

@tracer(trace_entity=True)
def fib(n):
    if n <= 1:
        return n
    return fib(n - 2) + fib(n - 1)

fib(3)
```

```text
-> fib(n=3)
|  -> fib(n=1)
|  |  <- fib returned 1
|  -> fib(n=2)
|  |  -> fib(n=0)
|  |  |  <- fib returned 0
|  |  -> fib(n=1)
|  |  |  <- fib returned 1
|  |  <- fib returned 1
|  <- fib returned 2
```

## 功能

- **调用树**：使用 `->` / `<-` 分层展示参数与返回值。
- **耗时统计**：单次调用耗时与按函数汇总的统计报告。
- **异常分析**：抛出点、完整调用栈、传播路径、被捕获/逃逸状态，可选局部变量快照与 JSON 导出。
- **统一输出管道**：控制台、文件路径、可调用对象、可写流或多目标输出，全部由 `output_way` 与 `overwrite` 控制。
- **仅终端着色**：ANSI 转义码不会写入文件目标。
- **零依赖**：仅使用标准库，要求 Python 3.10.9+。

## 安装

```bash
pip install pypi-tracer
```

发行包名为 `pypi-tracer`，导入包名为 `tracer`。

## 文档

- [快速开始](getting-started.md)
- [输出重定向](guide/output.md)
- [耗时统计](guide/time-tracing.md)
- [异常追踪](guide/exception-tracing.md)
- [API 参考](api.md)
- [架构设计](architecture.md)

## 许可证

MIT。参见 [LICENSE](https://github.com/Ricardo-shuo-liu/Tracer/blob/main/LICENSE)。
