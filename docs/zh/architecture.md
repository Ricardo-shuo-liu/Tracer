# 架构设计

## 模块划分

| 模块 | 职责 |
| --- | --- |
| `tracer/core/Tracer.py` | 公开的 `tracer` 装饰器与 `Tracer` 上下文管理器 |
| `tracer/core/TraceContext.py` | 每次运行的状态：输出缓冲、耗时、异常记录 |
| `tracer/core/Parser.py` | `sys.settrace` 回调；格式化 call/return/exception 事件 |
| `tracer/core/TraceStats.py` | 按函数聚合耗时并生成报告 |
| `tracer/core/Color.py` | 终端能力检测与 ANSI 辅助函数 |
| `tracer/exceptions/TraceError.py` | 异常记录、报告与 JSON 导出 |
| `tracer/writer/` | 输出规范化、分发与各目标 writer |

## 数据流

```text
@tracer(...) / Tracer(...)
        │
        ├── normalize_output_way(output_way)
        │          └── WorkFlow ──► Writer[] ──► FileWriter / 流 / 回调
        │
        └── TraceContext ──► sys.settrace(hook)
                                  │
                      Parser.frame_callback
                         ├── call    → "-> fn(args)"
                         ├── return  → "<- fn returned value"
                         └── exception → TraceErrors.observe()
                                  │
                            TraceContext.add()
                                  │
                         finish() → WorkFlow.forward()
```

## 设计决策

### 单点规范化

`normalize_output_way()` 只对公开的 `output_way` 做一次分类。它区分单目标（`None`、路径、可调用对象、可写流）与目标集合，避免把 `str`、`bytes`、`StringIO` 这类可迭代值误拆成逐字符或逐行的目标。

### 隔离式分发

`WorkFlow.forward()` 把每个输出块写入所有 `Writer`。某个目标失败不会阻止其余目标接收输出。第一个失败会交给输出层，由输出层转换为 `stderr` 警告，避免输出错误掩盖从被追踪代码中逃逸的异常。

### 按运行重置

`TraceContext.begin_run()` 在每次顶层运行开始时清空缓冲文本、耗时数据、异常记录与待处理异常帧。因此报告只描述刚刚结束的那次运行，不会跨调用累积。

### 钩子恢复

装饰器与上下文管理器在安装钩子前保存 `sys.gettrace()`，结束后恢复。这样嵌套的追踪器、调试器、覆盖率工具与 profiler 不会被破坏。

### 安全格式化

参数与返回值通过受保护的 `repr()` 格式化。即使对象的 `__repr__` 抛出异常，也只会显示占位文本，不会中断被追踪的调用。

### 颜色策略

只有当所有目标都是控制台类流时才启用 ANSI 码。由于文本在分发前就已着色，这一策略可以防止转义序列写入文件。

## 线程

`sys.settrace` 是线程局部的。只有进入装饰器或 `with` 块的线程会被追踪，其他线程不受钩子影响。
