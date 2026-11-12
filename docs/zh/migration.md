# 迁移指南

本页说明基于 writer 的输出管道带来的 API 变化。

## `logging_path` → `output_way`

`tracer` 装饰器与 `Tracer` 上下文管理器中的 `logging_path` 参数已移除，改用 `output_way`：

```python
# 旧写法
@tracer(trace_entity=True, logging_path="trace.log")
def run():
    ...

# 新写法
@tracer(trace_entity=True, output_way="trace.log")
def run():
    ...
```

### 控制台输出的变化

旧的 `logging_path` 实现会同时把追踪写入文件并打印到控制台。`output_way="trace.log"` 只写文件。若需要保留两个目标，请显式列出：

```python
@tracer(trace_entity=True, output_way=[None, "trace.log"])
def run():
    ...
```

`None` 表示控制台目标。默认控制台流现在是 `stderr`；此前追踪文本打印到 `stdout`。

### 文件格式的变化

旧实现使用 Python 的 `logging` 模块，每行带有时间戳前缀（`%(asctime)s | %(message)s`）。现在文件输出是纯追踪文本，与控制台输出一致，不再包含时间戳。

### 报告跟随输出目标

耗时报告与异常报告过去无论 `logging_path` 如何都打印到 `stdout`。现在它们与追踪文本走同一个 `output_way` 管道，因此文件目标会收到完整文档。

## 交互式参数已移除

以下参数已移除：

- `interactive`
- `interactive_on_event`
- `interactive_filter`

请使用 `breakpoint()`、`pdb.set_trace()` 或 IDE 调试器进行交互式检查。`tracer/interact` 模块及其测试已删除。

## `overwrite`

`overwrite=True` 会让每个文件目标在首次写入时截断，之后在 writer 生命周期内继续追加。它对可调用对象与流无效。允许混合目标列表，只有文件目标会被截断。

## 已移除的模块

`tracer/core/Log.py` 已删除。所有输出由 `tracer/writer/WorkFlow.py` 与 `tracer/writer/Writer.py` 处理。
