# API 参考

## `tracer`

```python
from tracer import tracer

tracer(
    trace_fn: list[Callable] | None = None,
    trace_entity: bool = False,
    output_way=None,
    overwrite: bool = False,
    time_trace: bool = False,
    use_color: bool = False,
    exception_trace: bool = False,
    show_locals: bool = False,
    exception_json_path: str | None = None,
) -> Callable
```

装饰器工厂，返回用于包装目标函数的装饰器。

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `trace_fn` | `None` | 需要额外追踪的函数，按 `__name__` 匹配 |
| `trace_entity` | `False` | 追踪被装饰函数本身 |
| `output_way` | `None` | 输出目标，参见[输出重定向](guide/output.md) |
| `overwrite` | `False` | 文件目标首次写入时截断 |
| `time_trace` | `False` | 启用单次耗时与统计报告 |
| `use_color` | `False` | 在控制台类目标上启用 ANSI 颜色 |
| `exception_trace` | `False` | 启用异常收集与报告 |
| `show_locals` | `False` | 在异常观测点采集局部变量 |
| `exception_json_path` | `None` | 将异常记录导出到该 JSON 文件 |

包装函数通过 `wrapped.tracer_ctx` 暴露实时上下文。

如果 `trace_entity` 为假且 `trace_fn` 为 `None`，追踪集合不受限制，钩子生效期间执行的所有帧都会被追踪。

## `Tracer`

```python
from tracer import Tracer

Tracer(
    trace_fn: list[Callable] | None = None,
    output_way=None,
    overwrite: bool = False,
    time_trace: bool = False,
    use_color: bool = False,
    exception_trace: bool = False,
    show_locals: bool = False,
    exception_json_path: str | None = None,
)
```

上下文管理器，配置项与装饰器相同，但没有 `trace_entity`。需要追踪的函数都应列入 `trace_fn`。

| 成员 | 说明 |
| --- | --- |
| `with Tracer(...) as t:` | 安装追踪钩子并返回实例 |
| `t.errors` | `TraceErrors` 收集器；`exception_trace=False` 时为 `None` |
| `t.stats` | `TraceStats` 收集器；`time_trace=False` 时为 `None` |

## 输出目标类型

`output_way` 接受：

- `None`：控制台（`sys.stderr`）。
- `str`、`bytes`、`os.PathLike`：UTF-8 文件输出。
- 可调用对象：对每个输出块调用。
- 带 `write()` 的对象：直接写入。
- 上述目标组成的可迭代对象：多目标分发。

非法类型会在创建装饰器或上下文管理器时抛出 `TypeError`。`overwrite=True` 但没有任何文件目标时抛出 `ValueError`。

## 运行生命周期

每次顶层调用（装饰器）或 `with` 块（上下文管理器）会依次执行：

1. 重置每次运行的状态（耗时、异常记录、缓冲行）。
2. 安装 `sys.settrace`，并保存此前生效的钩子。
3. 缓冲追踪文本。
4. 恢复此前的钩子。
5. 通过 `output_way` 写出缓冲文本、异常报告与耗时报告。

被装饰函数自身的递归由内部深度计数跟踪，嵌套调用不会重置运行状态或重复安装钩子。

## 公开收集器

### `TraceStats`

| 成员 | 说明 |
| --- | --- |
| `data` | 按函数名索引的 `dict[str, FuncStat]` |
| `format_report(setcolor=False)` | 返回统计报告字符串 |
| `print_report(setcolor=False)` | 将报告打印到 stdout |

### `TraceErrors`

| 成员 | 说明 |
| --- | --- |
| `records` | `list[ExcRecord]` |
| `handled` / `unhandled` | 作用域内被捕获 / 逃逸的记录 |
| `to_list()` | 可 JSON 序列化的记录列表 |
| `export_json(path)` | 直接将 JSON 文档写入 `path` |
| `format_report(setcolor=False)` | 返回异常报告字符串 |
| `print_report(setcolor=False)` | 将报告打印到 stdout |

## 已移除的 API

`logging_path` 以及交互式参数（`interactive`、`interactive_on_event`、`interactive_filter`）已不再属于 API。参见[迁移指南](migration.md)。
