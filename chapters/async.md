# Async

![[Think 2025-06-22 22.13.45.excalidraw]]
我们之所以很少自己实现协程库, 是因为实现协程库之后往往会发现, 我们只是实现了一版蹩脚的async特性. 那么什么是async呢?

async是语言为了支持异步IO而设计的一套协程调度机制. 它的目标是提高单线程IO效率, 提高吞吐量. 相比于原始的协程, 它更符合人体工学.

## Async提供的新特性

async在语言中提供两个概念.
首先, 它提供的一组关键词async和await, 使用这两个关键词能够更好的定义协程, 并且定义协程之间如何调度.
另外, 它提供一个协程队列(事件队列), 任何被挂起的协程都会入队, 可以运行的协程会出队进行执行. 这些队列在javascript中是隐式存在的, 在其他语言中需要显式定义.
![[Pasted image 20250606204340.png]]

- async关键词放在函数定义之前, 声明该函数是一个async function. 调用async function返回一个coroutine.
- 在异步函数调用前面放上await关键词, 表示被调用协程开始工作, 而本协程被 挂起, 被加入到队列之中. [参考](https://devblogs.microsoft.com/dotnet/how-async-await-really-works/#async/await-under-the-covers). 在被调用的协程完成工作返回之后, 但本协程被唤起, 检查await任务的状态是完成, 则会继续运行本协程后续的代码.

async特性十分容易理解, 以至于并不需要了解其背后的原理也能够使用. 至于背后的实现原理, 每种语言都略有不同, javascript使用Promise, 其他语言使用别的机制. 这里就不再深入了.

## 什么时候使用async

在IO密集而性能又至关重要的场景, 譬如需要读写大量文件, 读取大量url, 大量请求api, 访问数据库等等.

## 如何实现自己的async Function呢?

通常语言本身或标准库中会集成有各种async function, 譬如读写文件, 收发请求的等等. 很多库的作者也会提供相关async function. 而我们只需要await调用这些async function去组合实现自己的async function.
![[Pasted image 20250616222159.png]]

开发时, 一开始我们总是实现同步的版本, 然后进行性能测试, 有需要才改成async版本. 这样比一开始就使用async要更容易debug. 也不会进入提早优化程序的陷阱.
