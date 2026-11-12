# 异常追踪

异常追踪会观测被追踪作用域内抛出的每一个异常，并在运行结束后输出结构化报告。它不会吞掉或抑制异常：原始异常会按原路径继续传播。

## 参数

| 参数 | 默认值 | 含义 |
| --- | --- | --- |
| `exception_trace` | `False` | 异常分析总开关 |
| `show_locals` | `False` | 在异常首次被观测处采集局部变量快照 |
| `exception_json_path` | `None` | 运行结束后把所有记录写入该 JSON 文件 |

## 示例

```python
from tracer import tracer

def deep_untraced(n):          # 未加入 trace_fn
    if n < 0:
        raise ValueError(f"negative depth: {n}")
    return n * 2

def risky(n):
    return deep_untraced(n)

def swallowed():
    try:
        raise KeyError("swallowed_key")
    except KeyError:
        return "recovered"

@tracer(
    trace_fn=[risky, swallowed],
    trace_entity=True,
    exception_trace=True,
    show_locals=True,
)
def run():
    swallowed()
    return risky(-1)

try:
    run()
except ValueError:
    pass
```

因异常展开的帧会显示 `raised`，而不是 `returned`：

```text
-> run()
|  -> swallowed()
|  |  <- swallowed returned 'recovered'
|  -> risky(n=-1)
|  |  <- risky raised ValueError: negative depth: -1
|  <- run raised ValueError: negative depth: -1
```

随后输出报告：

```text
===== Exception Trace Report =====
total=2  unhandled=1  handled=1  by_type={'KeyError': 1, 'ValueError': 1}
----------------------------------
#1  KeyError: 'swallowed_key'
    status      : handled by swallowed()
    raised at   : swallowed() -> demo.py:13
    propagated  : swallowed
    stack (outermost -> raise point):
      File "demo.py", line 13, in swallowed
        raise KeyError("swallowed_key")
----------------------------------
#2  ValueError: negative depth: -1
    status      : escaped (unhandled within traced scope)
    raised at   : deep_untraced() -> demo.py:5
    propagated  : risky -> run
    stack (outermost -> raise point):
      File "demo.py", line 20, in run
        return risky(-1)
      File "demo.py", line 8, in risky
        return deep_untraced(n)
      File "demo.py", line 5, in deep_untraced
        raise ValueError(f"negative depth: {n}")
    locals at observation point:
      n = -1
----------------------------------
==================================
```

## 提取字段

| 字段 | 含义 |
| --- | --- |
| `exc_type` / `message` | 异常类名与实例的 `str()` |
| `raised at` | 异常真实抛出的函数、文件与行号 |
| `stack` | 完整 traceback，包含从未被追踪的中间帧 |
| `propagated` | 异常流经的被追踪函数，例如 `dive x4 -> safe` |
| `status` | 作用域内被捕获时为 `handled by fn()`，否则为 `escaped` |
| `locals` | 观测点的局部变量快照（`show_locals=True`） |

## 程序化访问

```python
with Tracer(trace_fn=[dive], exception_trace=True) as t:
    ...

t.errors.records      # list[ExcRecord]
t.errors.to_list()    # list[dict]，可 JSON 序列化
t.errors.unhandled    # 逃出追踪作用域的异常
t.errors.handled      # 在作用域内被捕获的异常
```

使用装饰器时，上下文挂在包装函数上：

```python
@tracer(trace_entity=True, exception_trace=True)
def run(): ...

run()
run.tracer_ctx.errors.to_list()
```

## JSON 格式

`exception_json_path` 写出的文档结构如下：

```json
{
  "summary": {
    "total": 2,
    "unhandled": 1,
    "handled": 1,
    "by_type": {"KeyError": 1, "ValueError": 1}
  },
  "exceptions": [
    {
      "seq": 1,
      "exc_type": "KeyError",
      "message": "'swallowed_key'",
      "status": "handled by swallowed()",
      "raised_at": {"func_name": "swallowed", "filename": "demo.py", "lineno": 13, "code_line": "raise KeyError(\"swallowed_key\")"},
      "handled_by": "swallowed",
      "escaped": false,
      "propagation_path": ["swallowed"],
      "stack": [],
      "locals": {}
    }
  ]
}
```

JSON 文件直接写入，不经过 `output_way`。如果写入失败，Tracer 会向 `stderr` 输出警告，不会覆盖原始异常。

## 范围

只有在追踪集合（`trace_entity` 或 `trace_fn`）命中的帧中才会观测异常。集合之外的帧仍会出现在 traceback 栈中，但不会被单独追踪。
