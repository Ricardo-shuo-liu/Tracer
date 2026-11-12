# 输出重定向

所有追踪文本与报告都经过同一条管道：

```text
TraceContext ──► WorkFlow ──► Writer ──► 目标
                               ├─ 控制台（stderr）
                               ├─ FileWriter
                               ├─ 可调用对象
                               └─ 可写流
```

`output_way` 在创建装饰器或上下文管理器时被规范化一次，单个目标与目标集合都可以接受。

## 默认输出

`output_way=None` 表示控制台，具体是 `sys.stderr`，而不是 `sys.stdout`。这样追踪输出可以与程序的正常输出分别重定向：

```python
@tracer(trace_entity=True)
def run():
    ...
```

```bash
python app.py 2> trace.log
```

## 支持的目标

| `output_way` 取值 | 行为 |
| --- | --- |
| `None` | 写入 `sys.stderr` |
| `str`、`bytes`、`os.PathLike` | 以 UTF-8 写入文件 |
| 可调用对象 | 对每个输出块调用 `target(text)` |
| 带 `write()` 的对象 | 调用 `target.write(text)` |
| 上述目标组成的可迭代对象 | 将每个输出块分发到所有目标 |

字符串、字节与 `pathlib.Path` 会被视为**一个**目标，而不是字符集合；流对象同理。

### 文件路径

```python
@tracer(trace_entity=True, output_way="trace.log")
def run():
    ...
```

### 可调用对象

```python
lines = []

@tracer(trace_entity=True, output_way=lines.append)
def run():
    ...
```

### 可写流

```python
import io

buffer = io.StringIO()

@tracer(trace_entity=True, output_way=buffer)
def run():
    ...

print(buffer.getvalue())
```

### 多目标

```python
@tracer(
    trace_entity=True,
    output_way=["trace.log", lines.append],
)
def run():
    ...
```

## overwrite 语义

`overwrite` 只作用于**文件目标**，对可调用对象和流无效。

- `overwrite=False`（默认）：向已有文件追加。
- `overwrite=True`：每个文件在首次写入时截断，之后在 writer 生命周期内继续追加。

```python
@tracer(trace_entity=True, output_way="trace.log", overwrite=True)
def run():
    ...
```

允许使用混合目标列表，例如 `["trace.log", callback]`：文件会被截断，回调不受影响。如果 `overwrite=True` 但完全没有文件目标，创建装饰器或上下文管理器时会抛出 `ValueError`。

## 缓冲

追踪文本会先缓冲，在顶层调用结束时一次性写出；耗时报告与异常报告随后输出。因此文件是在写出时打开的，而不是在装饰时打开。

## 失败处理

各个目标彼此隔离：

- 某个目标抛出异常时，其余目标仍会收到输出。
- 输出层会把失败信息写到 `stderr`，并且不会替换正在从追踪作用域向外传播的异常。

这意味着日志文件不可写不会把一次成功调用变成错误；但路径错误也会在运行结束后以警告形式出现，而不是在装饰时立即失败。

## 颜色安全

只有当所有目标都是控制台类流时才启用颜色，因此 ANSI 转义码不会写入文件或非终端缓冲区。参见[彩色输出](color.md)。

## JSON 导出

`exception_json_path` 是独立的产物，不经过 `output_way`。它会在异常报告之后写出 JSON 文件。参见[异常追踪](exception-tracing.md)。
