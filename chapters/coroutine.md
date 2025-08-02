# Coroutine

![[Think 2025-06-22 22.07.11.excalidraw]]

## 协程历史

在cpu还是单核的时代, 并发这个概念其实就已经存在了. 此时的并发, 主要是为了让计算机能够在同一时间段内同时响应多个任务. 为了响应多个任务, 计算机就不得不来回切换当前执行的上下文. 当时有两种设计思路, 第一种, 上下文切换由硬件和操作系统负责, 对应用程序而言是透明的, 每个应用程序都认为自己独占了机器. 这诞生了进程, 线程等概念; 而另一种设计思路是, 应用程序应该自己负责进行上下文切换, 每个线程都应该在运行一段时间后主动挂起自己, 让其他线程得以执行, 具体操作由程序员负责控制. 虽然这条路线最终并没有变得流行, 但线程挂起自己的能力被证明是非常有用的, 操作系统于是提供了yield函数(这里我们记作thread-yield, 为了跟后面的概念区别开), 调用thread-yield能够让线程挂起自己, 让操作系统去调度其他线程执行. 虽然我们能够主动挂起线程, 但是线程之间如何调度仍旧是操作系统负责的, 我想要在挂起线程A的时候, 让线程B继续执行, 这是办不到的, 因为下个执行的线程是操作系统决定的, 有可能是任何一个除了B以外的线程.
![[Pasted image 20250616214918.png]]

为了达到用户控制执行上下文切换的目标, 首先我们要绕过操作系统, 完全在用户态完成这项工作. 也是因为要绕过操作系统, 我们不能把任务分散到多个线程中, 而是集中在一个线程里, 然后提供一些新特性, 让应用程序能够在单线程中主动切换执行上下文.

## 协程引入的新特性

为了在用户态切换上下文, 引入了两个新的关键词, 一个叫做yield / co_yield, 另一个叫next / resume / cowait / await, 不同的语言中使用了不同的名字, 我们这里取python中的关键词命名进行后续说明, 也就是yield和next . 下面用一个例子来说明它们.
![[Think 2025-06-06 11.39.40.excalidraw]]

当某个函数function2中使用了yield关键词, 它就不再被当成一个普通函数, 调用它不会直接运行function2, 而是会生成一个特殊对象. 而在这个特殊对象上进行next操作, 执行上下文会切换到function2进行执行, 直到function2使用了yield, 执行上下文则切回调用它的地方, 此处是main函数. 而此时function2的上下文并没有被回收, 因为它还没有执行完. 在main中再次调用next会再次切回function2, 执行剩下的部分, 以此类推.
![[Think 2025-06-16 21.51.48.excalidraw]]
刚才我们提到了协程, 这里跟线程对比一下. 线程需要一个函数作为入口. 协程也是如此. 线程可以调用thread-yield去挂起自己. 协程可以通过yield把控制还给caller. 操作系统能够恢复线程的运行. caller能通过next恢复协程的运行. 所以很多人才为此命名协程, 为了跟线程对应起来.

![[Think 2025-06-16 21.59.55.excalidraw]]

在yield / co_yield和next / resume  / cowait / await这两个关键词之上, 一般语言还会发展出两个进阶关键词, 一个是yield from / yield*, 这个关键词可以让你在一个协程中“调用”另一个协程; 另一个是send, 可以让你在上下文切换的时候传值.
![[Think 2025-06-16 22.04.22.excalidraw]]

## 什么时候使用协程

那么什么时候使用协程这一套概念呢?
首先我们不会拿它去提升计算效率, 因为所有协程都运行在同一个线程中, 所以不会提升计算效率. 但是, 我们有可能使用它去提升IO效率, 尤其是需要等待IO完成的场景, 可以挂起协程, 然后运行其他协程.
尽管如此, 实际工作中, 我们基本不会自己去开发一套协程库去调度协程来提升IO效率, 而是直接使用语言提供的async特性. yield / resume机制比async要更加底层, 完整实现一套调度机制需要很多工作, 不如直接使用更加完善的async特性.

日常工作中, 我们会使用yield和resume快速实现业务相关的生成器或者状态机.

### 生成器

生成器是一种对象, 提供next方法和一个类似StopIteration的exception, 或者提供next方法和finished方法.
生成器可以放到循环中, 就像遍历一个Array. 但它的优势是lazy execution, 在你需要值的时候才去算一个出来. 像是无限数列就可以用生成器进行抽象. 使用生成器可以让一些函数式的代码变得更加简单, 这里先不展开.

```python
def my_generator(n):
 for i in range(n):
  yield i

gen = my_generator(5)
for value in gen:
 print(value)
```

### 状态机

状态机也是一种对象, 它拥有一组状态, 根据它当前的状态和用户输入, 决定它的输出(或副作用)以及下一个状态. 用yield和send可以很方便的实现一个简易的有限状态机.

```python
def traffic_light():
 state = "red"
 yield state

 while True:
  input_ = yield state
  if input_ == "PedestrianWaiting" and state == "green":
   state = "red"
  elif input_ == "CarWaiting" and state == "red":
   state = "green"

light = traffic_light()
assert light.send("CarWaiting") == "green"
assert light.send("PedestrianWaiting") == "red"
```

总之, 一些能够执行, 同时需要保留状态的对象, 我们都可以尝试使用协程去实现, 只要用协程实现更简便.
除此之外, 一般我们都会尽可能缩小yield / resume的使用范围. 在代码中不加审慎的使用协程会让代码变得难以理解.
