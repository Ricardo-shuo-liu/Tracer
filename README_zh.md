# Tracer

- 本项目灵感来自UC伯克利的课程CS61A 

- 使用`tracer`装饰器和`Tracer`上下文管理器来追踪函数的调用情况

### 使用`tracer`装饰器

- 你可以查看`tests\core\test_tracer.py`内容
```
from tracer import tracer

def add(x,y):
    return x + y


def chain(n):
    if n <= 1:
        return add(1,1)
    return add(n, chain(n-1))

@tracer(trace_fn=[add, chain],
        trace_entity=True)
def fun():
    return chain(3)

@tracer(trace_entity=True)
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-2) + fib(n-1)
if __name__ == "__main__":
    fun()
    print()
    fib(3)
```
执行结果如下:
```
-> fun()
|  -> chain(n=3)
|  |  -> chain(n=2)
|  |  |  -> chain(n=1)
|  |  |  |  -> add(x=1, y=1)
|  |  |  |  |  <- add returned 2
|  |  |  |  <- chain returned 2
|  |  |  -> add(x=2, y=2)
|  |  |  |  <- add returned 4
|  |  |  <- chain returned 4
|  |  -> add(x=3, y=4)
|  |  |  <- add returned 7
|  |  <- chain returned 7
|  <- fun returned 7

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

### 使用`Tracer`上下文管理器

- 你可以查看`tests\core\test_Tracer.py`内容
```
from tracer import Tracer


def add(x,y):
    return x + y


def chain(n):
    if n <= 1:
        return add(1,1)
    return add(n, chain(n-1))

def fun():
    return chain(3)

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-2) + fib(n-1)
    
if __name__ == "__main__":
    with Tracer(trace_fn=[add,chain,fun,fib]):
        fun()
        print()
        fib(3)
```
执行结果如下：
```
-> fun()
|  -> chain(n=3)
|  |  -> chain(n=2)
|  |  |  -> chain(n=1)
|  |  |  |  -> add(x=1, y=1)
|  |  |  |  |  <- add returned 2
|  |  |  |  <- chain returned 2
|  |  |  -> add(x=2, y=2)
|  |  |  |  <- add returned 4
|  |  |  <- chain returned 4
|  |  -> add(x=3, y=4)
|  |  |  <- add returned 7
|  |  <- chain returned 7
|  <- fun returned 7

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

需要注意的是`Tracer`上下文管理器没有提供`trace_entity：bool`接口

### Tracer的设计功能
---
1. 日志功能

- 基于`logging`模块 
- 通过`tracer`和`Tracer`的`logging_path`实现启用
- `logging_path` 默认数值为 `None` 如果传入真实地址 那么认为该真实地址为log的存储位置

你可以查询 `tests/core/test_log_tracer.py` 和 `tests/core/test_log_Tracer.py` 了解如何使用
---
2. 时间追踪

- 基于`time` 和 `dataclass` 模块
- 通过标识`frame`实现唯一纪律
- 通过`tracer`和`Tracer`的`time_trace`实现启用
- `time_trace` 默认数值为 `False` 修改为`True` 认为是启用

Example:
```
from tracer import tracer

def add(x,y):
    return x + y


def chain(n):
    if n <= 1:
        return add(1,1)
    return add(n, chain(n-1))

@tracer(trace_fn=[add, chain],
        trace_entity=True,
        logging_path="/home/ricaedo/Tracer/test.log",
        time_trace=True)
def fun():
    return chain(3)

@tracer(trace_entity=True,logging_path="/home/ricaedo/Tracer/test.log",time_trace=True)
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-2) + fib(n-1)
if __name__ == "__main__":
    fun()
    print()
    fib(3)
```
输出:
```
-> fun()
|  -> chain(n=3)
|  |  -> chain(n=2)
|  |  |  -> chain(n=1)
|  |  |  |  -> add(x=1, y=1)
|  |  |  |  |  <- add returned 2 | cost=0.000013s
|  |  |  |  <- chain returned 2 | cost=0.000042s
|  |  |  -> add(x=2, y=2)
|  |  |  |  <- add returned 4 | cost=0.000012s
|  |  |  <- chain returned 4 | cost=0.000092s
|  |  -> add(x=3, y=4)
|  |  |  <- add returned 7 | cost=0.000012s
|  |  <- chain returned 7 | cost=0.000150s
|  <- fun returned 7 | cost=0.000223s

===== Function Trace Statistics Report =====
Function        Calls   Total(s)  Avg(s)    Min(s)    Max(s)    
add             3       0.0000    0.0000    0.0000    0.0000    
chain           3       0.0003    0.0001    0.0000    0.0001    
fun             1       0.0002    0.0002    0.0002    0.0002    
============================================


-> fib(n=3)
|  -> fib(n=1)
|  |  <- fib returned 1 | cost=0.000012s
|  -> fib(n=2)
|  |  -> fib(n=0)
|  |  |  <- fib returned 0 | cost=0.000011s
|  |  -> fib(n=1)
|  |  |  <- fib returned 1 | cost=0.000011s
|  |  <- fib returned 1 | cost=0.000059s
|  <- fib returned 2 | cost=0.000115s

===== Function Trace Statistics Report =====
Function        Calls   Total(s)  Avg(s)    Min(s)    Max(s)    
fib             5       0.0002    0.0000    0.0000    0.0001    
============================================
```
关于上下文管理器`Tracer`启用相关功能可以查看`tests/core/test_time_Tracer.py`

