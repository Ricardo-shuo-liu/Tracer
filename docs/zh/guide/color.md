# 彩色输出

通过 `use_color=True` 启用 ANSI 颜色：

```python
@tracer(trace_entity=True, use_color=True)
def run():
    ...
```

颜色只作用于核心追踪内容：函数名、返回值、耗时、报告表头与异常状态行。其余输出保持不变。

## 颜色支持检测

Tracer 在导入时检测终端是否支持颜色：

- Unix：`sys.stderr.isatty()` 必须为真，且 `tput colors` 至少报告 8 色。
- Windows 10 build 10586 或更高：为标准错误句柄启用控制台模式。

检测结果保存在 `tracer.core.Color.COLOR_SUPPORT`。如果终端不支持颜色，`use_color=True` 不产生任何效果，也不会输出转义序列。

## 文件不会收到 ANSI 码

只有当**所有**目标都是控制台类流时才启用颜色：

- `None`（默认控制台目标）
- `sys.stdout` 或 `sys.stderr`
- `isatty()` 返回 `True` 的流

只要目标中包含文件、可调用对象或非终端流，整次运行都会禁用颜色。这是有意为之：追踪文本在分发到各目标之前就已着色，如果对混合目标启用颜色，转义序列会写入文件。

```python
# 不会着色：否则文件会收到 ANSI 码。
@tracer(trace_entity=True, use_color=True, output_way=["trace.log", sys.stderr])
def run():
    ...
```

需要颜色时，使用纯控制台目标：

```python
@tracer(trace_entity=True, use_color=True, output_way=sys.stderr)
def run():
    ...
```
