# Tracer

\- This project is inspired by the CS61A course of UC Berkeley\.

\- It adopts the `tracer` decorator and `Tracer` context manager to track function calls\.

### Using the `tracer` Decorator

\- Refer to the file `tests\core\test_tracer.py` for details\.

```python
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

**Execution Output:**

```plain text
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

### Using the `Tracer` Context Manager

\- Refer to the file `tests\core\test_Tracer.py` for details\.

```python
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

**Execution Output:**

```plain text
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

**Note:** The `Tracer` context manager does not provide the `trace_entity: bool` interface\.

### Tracer Core Functionalities

---

#### 1\. Logging Function

- Implemented based on the built\-in `logging` module\.

- Enabled via the `logging_path` parameter of both the `tracer` decorator and `Tracer` context manager\.

- `logging_path` defaults to `None`\. If a valid file path is passed, logs will be persisted to the specified path\.

Refer to `tests/core/test_log_tracer.py` and `tests/core/test_log_Tracer.py` for usage examples\.

---

#### 2\. Time Tracing

- Implemented based on the `time` and `dataclass` modules\.

- Unique call records are identified via frame markers\.

- Enabled via the `time_trace` parameter of `tracer` and `Tracer`\.

- `time_trace` defaults to `False`\. Set it to `True` to enable time tracing\.

**Example Code:**

```python
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

**Execution Output:**

```plain text
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

Refer to `tests/core/test_time_Tracer.py` for time tracing usage with the `Tracer` context manager\.

---

#### 3\. Startup Interactive Inspection

- Implemented based on the `code.interact` module\.

- Enabled via the boolean parameter `interactive`\.

- When enabled, an interactive shell will be launched for real\-time data inspection\.

**Example Code:**

```python
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

**Execution Output:**

```plain text
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

This parameter is also supported by the`Tracer` context manager\. Refer to `tests/interact/test_Tracer_interact.py` for usage demonstrations\.

---

#### 4\. Key Event Terminal Interaction

- Implemented based on the `code.interact` module\.

- Enabled via the boolean parameter `interactive_on_event`\.

- When enabled, an interactive shell will pop up at key execution nodes for data inspection\.

**Example Code:**

```python
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

**Execution Output:**

```plain text
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

After enabling `interactive_on_event`, interactive shells will be triggered at the **start** and **return** moments of all traced functions\.

This parameter is also compatible with the `Tracer` context manager\. Refer to `tests/interact/test_Tracer_interact_on_event.py` for relevant examples\.

**Important Notes:**

Enabling `interactive_on_event` is **not recommended** in most scenarios\. To preserve terminal stability, the tool suppresses `SystemExit`, `EOFError`, and `ValueError`, which may cause the program to be unclosable except by terminating the terminal process\. Additionally, each function triggers two interactive sessions \(on entry and return\), leading to severe efficiency degradation in large\-scale program execution\.

**Only enable this parameter if you fully understand its working mechanism and usage scenarios\.**
