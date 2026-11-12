# 更新日志

## 未发布

### 新增

- 基于 writer 的输出管道（`WorkFlow`、`Writer`、`FileWriter`），提供 `output_way` 与 `overwrite`。
- 支持控制台、文件路径（`str`/`bytes`/`os.PathLike`）、可调用对象、可写流以及多目标输出。
- 每次运行重置耗时数据与异常记录。
- trace 钩子中的安全 `repr()` 格式化。
- 恢复此前安装的 `sys.settrace` 钩子。
- 基于 mkdocs-material 的中英双语文档。

### 变更

- 默认输出改为 `stderr`。
- 耗时报告与异常报告通过 `output_way` 写出，而不是打印到 `stdout`。
- 只有当所有目标都是控制台类流时才启用颜色；ANSI 码不会写入文件。
- 异常 JSON 导出增加错误保护，写入失败不会掩盖原始异常。
- `overwrite=True` 只作用于文件目标，并允许用于混合目标列表。

### 移除

- `logging_path`（请使用 `output_way`）。
- `interactive`、`interactive_on_event`、`interactive_filter`。
- `tracer/interact/` 及其测试。
- `tracer/core/Log.py`。
