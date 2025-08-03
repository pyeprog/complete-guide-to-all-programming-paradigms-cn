# Declarative Concurrency

接下来, 我们在declarative model上引入并发的概念, 形成声明式并发模型.

## 新增的特性

首先要引入的概念是线程, 相比进程, 创建和维护线程的开销小, 线程之间协同也比进程容易, 因此线程是更为流行的并发机制.

:::{figure} ../material/process-vs-thread.jpg
:width: 100%
:align: center

启动任意一个程序, 操作系统都会创建一个进程来维护程序运行上下文, 每一个进程就像一个独立的工厂, 内存空间是彼此独立的, 要协同工作相对困难. 而线程就像工厂中的一个个车间, 它们独立运行, 但又能够访问共同的一块内存空间, 因此协作起来比较方便. 而且创建并维护线程的开销比进程要小的多.
:::

但我们从顺序执行模型(sequential model)转换到并发模型(concurrency model), 实际上引入了好几个问题
:::{figure} ../material/challenge-of-concurrency
:width: 100%
:align: center

1. 怎么创建线程, 确保它能够工作? 这涉及到线程的创建.
2. 怎么才能拿到它的工作成果? 这涉及到线程的协同. 它包括两个子问题:
    1. 什么时候拿?
    2. 怎么拿?
3. 能在一个线程里停止另一个线程吗? 这涉及到线程的管理.

:::

在declarative model上引入了thread的概念, 实际上只解决了创建线程的问题. 但并不解决线程协同和管理的问题. 我们需要后续更强而有力的模型来解决.

## 创建线程

说到创建线程. 在所有语言中, `最主流的创建线程方式是以函数作为入口启动线程`. 绝大部分常见语言都是如此. 这样做有诸多好处, 譬如上下文管理简单, 结构清晰等等.
::::{tab-set}

:::{tab-item} java

```{code} java
:linenos:

class MyThread extends Thread {
    @Override
    public void run() {
        // do actual work here
    }
}

public class Demo {
    public static void main(String[] args) {
        MyThread thread = new MyThread();
        thread.start();  // spawn a thread and call its run method implicitly
    }
}
```

:::

:::{tab-item} rust

```{code} rust
:linenos:

use std::thread

fn main() {
    let mut children = vec![];
    
    for i in 0..10 {
        // spawn thread and add its handler to children
        children.push(thread::spawn(move || {
            // do actual work here
        }));
    }
    
    for child in children {
        let _ = child.join();
    }
}
```

:::

:::{tab-item} go

```{code} go
:linenos:

func work() {
    // do actual work here
}

func main() {
    go work()  // spawn goroutine(light-thread) to do the work
}
```

:::

:::{tab-item} elixir

```{code} elixir
:linenos:

func = fn ->
    # do actual work here
    end
pid = spawn(func)  # spawn a process(light-thread) to do the work
```

:::

::::

少部份语言支持一种更为自然的创建线程方式, 即把代码块, 甚至表达式作为线程主体. 这样的好处是代码更自然, 但自然的代价是, 它需要更多其他的概念来支持其正确运行. 譬如如果以表达式作为主体启动线程. 其他线程在需要该表达式求值的时候, 自动的等待表达式线程结束并得到他的值. {abbr}`这种机制不太普遍(OZ这种语言支持如此创建线程, 但它需要一种叫做dataflow variable的机制来在线程之间获取计算结果. 但这并不主流. 主流依然是以函数作为主体创建线程)`

::::{tab-set}

:::{tab-item} 表达式作为线程主体

```{code} oz
:linenos:
:filename: expr_as_entry.oz

declare X in 
X = thread 10 * 10 end + 100 * 100
{Browse X}
```

:::

:::{tab-item} 代码快作为线程主体

```{code} oz
:linenos:
:filename: block_as_entry.oz

declare X0 X1 X2 X3 in
thread
    Y0 Y1 Y2 Y3 in
        {Browse [Y0 Y1 Y2 Y3]}
        Y0 = X0 + 1
        Y1 = X1 + Y0
        Y2 = X2 + Y1
        Y3 = X3 + Y2
        {Browse completed}
end
{Browse [X0 X1 X2 X3]}
```

:::

::::

## 什么时候使用这种简易的并发模型？

如果仅仅创建一堆线程，却不支持它们之间的协作，甚至让它们彼此毫不知情，这样的并发有用吗？\
我只能说`用处有限`。因为线程只能独立处理任务，并与系统进行IO交互，即使任务完成，整个程序也难以正常退出。总之，在线程之上，我们还需要更多机制，才能真正解决复杂的并发任务。
:::{figure} ../material/no-normal-exit.jpg
如果工作线程完成工作后静默释放, 主线程无法判断工作线程是否结束
:::

## 系统级线程 Vs 轻量级线程

虽然声明式并发模型非常简洁，仅增加线程(thread)这一个概念, 但这不代表线程的设计就无关紧要. 在同一台机器上，能够顺畅开启十万线程与只能启动几千个线程有本质区别。面向并发编程时，能够开启更多线程自然意味着更强的能力。  

许多语言提供的线程实际上是在系统级线程上做了简单封装，创建此类线程需进行系统调用，线程调度由操作系统控制。它的优点是实现简单，缺点是能力上限受到操作系统限制。  

而面向并发编程设计的语言通常提供如green-thread, light-thread, goroutine等轻量级“线程”。谓“轻量级线程”实际上是概念上的线程，底层仍依赖系统线程执行，但调度由语言[运行时](https://en.wikipedia.org/wiki/Runtime_system)自行控制，切换效率更高，创建开销更小。更重要的是，使用上系统线程与轻量级线程无异，对用户而言堪称“白赚”的性能提升。
