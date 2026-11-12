# 快速开始

## 环境要求

- Python 3.10.9 或更高版本。
- 无第三方运行时依赖。

## 安装

从 PyPI 安装：

```bash
pip install pypi-tracer
```

从源码安装：

```bash
git clone https://github.com/Ricardo-shuo-liu/Tracer.git
cd Tracer
pip install -e .
```

发行包名为 `pypi-tracer`，导入时使用 `tracer`。

## 追踪一个函数

```python
from tracer import tracer

def add(x, y):
    return x + y

@tracer(trace_fn=[add], trace_entity=True)
def run():
    return add(1, 2)

run()
```

输出：

```text
-> run()
|  -> add(x=1, y=2)
|  |  <- add returned 3
|  <- run returned 3
```

`trace_entity=True` 会把被装饰函数本身加入追踪集合；`trace_fn=[...]` 用于加入其他函数。

## 使用上下文管理器

`Tracer` 无需装饰入口函数：

```python
from tracer import Tracer

def add(x, y):
    return x + y

with Tracer(trace_fn=[add]):
    add(1, 2)
```

上下文管理器没有 `trace_entity` 参数，需要追踪的函数都应列入 `trace_fn`。

## 选择追踪范围

Tracer 按函数**名称**匹配帧：

- `trace_entity=True` 加入被装饰函数的 `__name__`。
- `trace_fn=[f, g]` 加入 `f.__name__` 与 `g.__name__`。
- 两者都未提供时，追踪集合不受限制，钩子生效期间执行的所有帧都会被追踪。参见[已知限制](limitations.md)。

## 配置输出

默认输出到控制台（`stderr`）。通过 `output_way` 可以指定任意受支持的目标：

```python
@tracer(trace_entity=True, output_way="trace.log")
def run():
    ...
```

`output_way` 还支持可调用对象、可写流以及多目标列表。完整说明见[输出重定向](guide/output.md)。

## 下一步

- [输出重定向](guide/output.md)
- [耗时统计](guide/time-tracing.md)
- [异常追踪](guide/exception-tracing.md)
- [彩色输出](guide/color.md)
- [API 参考](api.md)
