# Tracer

一个轻量级的 Python 函数调用侵入式追踪器。

[![PyPI](https://img.shields.io/pypi/v/pypi-tracer.svg)](https://pypi.org/project/pypi-tracer/)
[![Python](https://img.shields.io/pypi/pyversions/pypi-tracer.svg)](https://pypi.org/project/pypi-tracer/)
[![License](https://img.shields.io/github/license/Ricardo-shuo-liu/Tracer.svg)](LICENSE)

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

从源码安装：

```bash
git clone https://github.com/Ricardo-shuo-liu/Tracer.git
cd Tracer
pip install -e .
```

## 快速开始

```python
from tracer import tracer

def add(x, y):
    return x + y

@tracer(trace_fn=[add], trace_entity=True)
def run():
    return add(1, 2)

run()
```

如果不想装饰入口函数，可以使用上下文管理器：

```python
from tracer import Tracer

with Tracer(trace_fn=[add]):
    add(1, 2)
```

输出可以写入文件、可调用对象、流或多个目标：

```python
@tracer(trace_entity=True, output_way="trace.log", overwrite=True)
def run():
    ...
```

## 文档

完整文档位于 [`docs/`](docs/index.md)，中文文档位于 [`docs/zh/`](docs/zh/index.md)：

- [快速开始](docs/zh/getting-started.md)
- [输出重定向](docs/zh/guide/output.md)
- [耗时统计](docs/zh/guide/time-tracing.md)
- [异常追踪](docs/zh/guide/exception-tracing.md)
- [API 参考](docs/zh/api.md)
- [架构设计](docs/zh/architecture.md)
- [已知限制](docs/zh/limitations.md)
- [迁移指南](docs/zh/migration.md)

本地构建文档站：

```bash
pip install -r docs/requirements.txt
mkdocs serve
```

## 环境要求

- Python 3.10.9 或更高版本。
- 无第三方运行时依赖。

## 许可证

MIT。参见 [LICENSE](LICENSE)。
