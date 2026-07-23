# Tracer

- 本项目灵感来自UC伯克利的课程CS61A 

- 使用`tracer`装饰器和`Tracer`上下文管理器来追踪函数的调用情况

---
### 开始使用Tracer

你可通过clone `Tracer`的Github仓库
```
git clone https://github.com/Ricardo-shuo-liu/Tracer.git

cd Tracer

# 启动你的环境
conda activate yourEnv
# 这里只是示范 你当然可以选择uv或者venv

pip install -e .
```

或者通过`Pypi`直接下载 

```
conda activate yourEnv

pip install pypi-tracer
```

- 这里需要说明的是`pip`下载的项目名称为`pypi-tracer`因为`pypi`不允许重名
- 但是在导入的时候 最高级包为`tracer`


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

3. 开始时的交互式检查

- 基于`code.interact` 模块
- 通过 `interactive:bool`启用
- 启用后会进入`shell`交互可以查看数据内容

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
        interactive=True)
def fun():
    return chain(3)

@tracer(trace_entity=True,
        logging_path="/home/ricaedo/Tracer/test.log",
        interactive=True)
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
运行结果:
```
==== Tracer Interactive Shell ====

===+fun()+===

>>> exit()

[Tracer] Interactive exit: SystemExit

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


==== Tracer Interactive Shell ====

===+fib(3)+===

>>> exit()

[Tracer] Interactive exit: SystemExit
3
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

当然在`Tracer`上下文管理器也支持该参数
你可以访问`tests/interact/test_Tracer_interact.py`查看使用示范

4. 关键节点启动终端交互

- 基于`code.interact` 模块
- 通过 `interactive_on_event:bool`启用
- 启用后会进入`shell`交互可以查看数据内容

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
        interactive_on_event=True)
def fun():
    return chain(3)

@tracer(trace_entity=True,
        logging_path="/home/ricaedo/Tracer/test.log",
        interactive_on_event=True)
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-2) + fib(n-1)
if __name__ == "__main__":
    fib(2)

```
运行结果:

```
==== Tracer Interactive Shell ====

===+fib(n=2)+===

>>> exit()

[Tracer] Interactive exit: SystemExit

==== Tracer Interactive Shell ====

===+fib(n=0)+===

>>> exit()

[Tracer] Interactive exit: SystemExit

==== Tracer Interactive Shell ====

===+fib returned 0====

>>> exit()

[Tracer] Interactive exit: SystemExit

==== Tracer Interactive Shell ====

===+fib(n=1)+===

>>> exit()

[Tracer] Interactive exit: SystemExit

==== Tracer Interactive Shell ====

===+fib returned 1====

>>> exit()

[Tracer] Interactive exit: SystemExit

==== Tracer Interactive Shell ====

===+fib returned 1====

>>> exit()

[Tracer] Interactive exit: SystemExit
-> fib(n=2)
|  -> fib(n=0)
|  |  <- fib returned 0
|  -> fib(n=1)
|  |  <- fib returned 1
|  <- fib returned 1
```

启动`interactive_on_event:bool`后会在追踪函数的开始和`Return`时候启动交互式

当然在`Tracer`也支持这个参数
你可以查看`tests/interact/test_Tracer_interact_on_event.py`了解相关的example

- 需要注意的是！一般情况下,并不建议开启`interactive_on_event:bool`,因为对于终端的保存,必须要屏蔽`SystemExit` `EOFError` `ValueError` 这些Error可能导致停止程序只能通过销毁终端的方式,而且由于每个函数近乎需要进入两次交互,在大规模的情况下这可能不是一个好的选择

- 你必须知道你要干什么,否则不建议启用`interactive_on_event:bool`

5. 关键节点选择性终端交互

- 基于`code.interact` 模块
- 通过 `interactive_filter:List[Callable]|None`启用
- 启用后会进入`shell`交互可以查看数据内容
- `interactive_filter:List[Callable]|None`默认数值为`None` 此时认为没有选者的节点
- `interactive_filter:List[Callable]|None` 如果设置应该为`trace_fn`的子集
- `interactive_filter:List[Callable]|None` 可以和 `interactive_on_event:bool`共用 这个时候实际效果和只启动`interactive_on_event:bool`是一样的
- 相较于`interactive_on_event:bool`的深度的追踪`interactive_filter:List[Callable]|None`能做到更精细的控制 所以更推荐使用`interactive_filter:List[Callable]|None`

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
        use_color=True)
def fun():
    return chain(3)

@tracer(trace_entity=True,
        logging_path="/home/ricaedo/Tracer/test.log",
        use_color=True,
        time_trace=True)
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
运行结果:
```
==== Tracer Interactive Shell ====

===+add(x=1, y=1)+===

>>> exit()

[Tracer] Interactive exit: SystemExit

==== Tracer Interactive Shell ====

===+add returned 2====

>>> exit()

[Tracer] Interactive exit: SystemExit

==== Tracer Interactive Shell ====

===+add(x=2, y=2)+===

>>> exit()

[Tracer] Interactive exit: SystemExit

==== Tracer Interactive Shell ====

===+add returned 4====

>>> exit()

[Tracer] Interactive exit: SystemExit

==== Tracer Interactive Shell ====

===+add(x=3, y=4)+===

>>> exit()

[Tracer] Interactive exit: SystemExit

==== Tracer Interactive Shell ====

===+add returned 7====

>>> exit()

[Tracer] Interactive exit: SystemExit
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
```

对于上下文管理器`Tracer`可以查看`tests/interact/test_Tracer_interactive_filter.py`了解如何使用

6. 色彩修正

- 基于模块`sys` `platform` `subprocess`实现
- 通过`use_color:bool`启动
- 对于部分不支持色彩输出的操作系统 如果启动`use_color`不会有任何效果(乱码屏蔽)
- 色彩修正是对部分核心内容进行色彩处理 而不是终端的所有内容都会被色彩修正
- 需要注意如果启动色彩修正 那么`log`存储的内容中会出现乱码 这是字符串拼接的原因 所以最好关闭`log`

对于`tracer`装饰器 运行`tests/core/test_tracer_color.py`了解效果和使用方法
对于`Tracer`上下文管理器 运行`tests/core/test_Tracer_color.py`了解效果和使用方法