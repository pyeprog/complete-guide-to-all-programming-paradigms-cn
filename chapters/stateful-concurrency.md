# Stateful Concurrency

![[Think 2025-06-22 21.40.47.excalidraw]]
现在我们要从explicit state model上继续前进. 第一站, 如何让其支持并发.

## 变量可修改时并发会导致什么问题

当变量不可修改时, 可以认为变量是只读的, 因此不同线程操作同一个变量时不会有读与写竞争或者写与写竞争. 这是declarative concurrency之所以简单的原因.

而当变量可以修改时, 故事就完全不一样了, 多个线程可以同时读写同一个变量, 而变量本身的读写在机器指令级别并不是原子操作. 譬如两个线程同时执行a++的时候, 因为操作系统切换运行线程的关系, 其机器指令可能交织在一起, 而交织成什么样子是随机的. 其中有正确的, 也有错误的交织. 因此不同线程同时写变量可能导致错误数据, 同时读和写也可能读到脏数据.
![[Think 2025-06-16 14.59.37.excalidraw]]

变量对每个线程都可见, 因此这种模型也被称为共享内存模型. 共享内存模型的主要目标是, 在同类线程竞争操作同一组状态(变量)的时候, 保证其正确性. 另外, 它还有另外一个目标, 即通过共享内存的方式, 让线程之间可以协作完成任务.

## Stateful Concurrency引入的新概念

共享内存模型引入了两个新概念: lock和condition variable.
当然也有不少材料和书籍会提到[mutex和semaphore](https://barrgroup.com/blog/mutexes-and-semaphores-demystified)这两个概念. 我们去掉这两个概念是因为:
mutex在使用上和lock没有区别, 两者几乎是等同的概念. 有些语言仅支持lock, 另一些仅支持mutex, 还有一些会以mutex作为互斥的原语, lock是对mutex的封装, 提供一些特殊的锁操作. 另外在操作系统级别, mutex也用来代指系统级的互斥量, 能够跨进程互斥. 但在同一个语言中, 我们只需要了解lock即可.

而semaphore则是另一个更高级的概念, 使用semaphore可以同时做到lock和condition variable的功能. semaphore允许N个线程同时进入临界区, 当N=1时, 它就是lock. 如果一个线程专门acquire semaphore, 另一个专门release semaphore, 于是我们就有了生产者和消费者, 也就做到了condition variable的工作. 不过semaphore更多还是一个学术概念. 无论硬件还是操作系统极少把semaphore作为互斥原语的. 所以这个概念可以先忽略.

我们只需要专注在lock和condition variable两个概念上即可.

- lock防止竞争读写同一块内存导致的错误
- condition variable让线程可以主动休眠和恢复, 以达到协同的目的

## 防止竞争读写导致的错误

一条语句可能对应若干条机器指令, 而站在程序角度, 系统如何调度线程是不可知的, 具体执行起来指令会穿插交织在一起. 在所有交织的可能性中, 会存在  一些错误的case. 如果能让错误的case不发生, 我们就能保证并发的正确性.
如何让这些错误的case不发生呢? 我们有两个策略, 一个是防止错误case的发生, 一个是发生错误时补救.
![[Think 2025-06-03 11.40.08.excalidraw]]

### 策略1: 使用lock防止错误case的发生

我们使用lock去防止错误的case发生.
![[Think 2025-06-16 20.17.16.excalidraw]]
lock和unlock是原子操作, 使用时一定成对出现. 如果临界区中的代码有可能报错退出, 我们需要catch错误, 并在final中进行unlock. java中就是如此.
golang中提供了defer关键词, 可以在函数正常或异常退出时执行unlock操作.
而一些语言提供了隐式的unlock, 譬如从c++11提供的lock_guard, 在退出scope的时候自动执行unlock.
无论显式还是隐式, lock和unlock总要成对出现, 并且一定要确保unlock能够被运行.

lock非常的简单, 但是同时也存在一些硬伤.

#### 硬伤1: 不可重入(同一个线程两次lock会死锁)

原始的lock有一个最直接的硬伤. 那就是同一个线程lock操作两次就会死锁. 日常应用中这很常见, 譬如在临界区中调用了另一个函数, 而这个函数刚好也需要使用lock, 这种情况下一旦调用了该函数, 就等于在同一个线程中重复获取锁, 这会导致死锁. 为了解决这个问题, 我们就引入了一种更高级的锁, reentrant lock(或者叫recursive_mutex), 在同一个线程中, 多次lock是不会导致死锁的.
![[Think 2025-06-16 20.43.14.excalidraw]]

#### 硬伤2: 性能问题

lock还导致了性能问题.
如果有些进程读, 有些进程写, 它们彼此互斥这没问题, 但如果两个线程都是读, 彼此还互斥就没有必要. 我们只需要保证读写互斥, 写写互斥即可. 这引入了另一种更高级的锁, reentrant read write lock. 这种锁提升了读性能. 在读多写少的时候适用.
![[Think 2025-06-16 21.12.03.excalidraw]]

#### 硬伤3: 死锁

最后是死锁问题.
死锁的问题更是被研究多年, 已经是老生常谈了. 死锁发生在多线程获取多个锁的时候. 解决死锁同样有两种策略, 防止和补救.
防止死锁有两种办法, 第一种, 按照固定顺序获取锁, 这种是最简单的方式. 第二种, 一次性try_lock所有的锁, 如果有一个失败就从头再来, 这种能够保证一次性获取所有锁.
补救死锁有两种办法, 第一种, 给锁定一个过期时间, 一旦超时就释放. 第二种, 让锁变得可以抢占, 这需要引入优先级的概念, 一旦高优先级的线程申请锁, 持有锁的低优先级的线程就报错, 并释放锁.
![[Think 2025-06-16 21.18.45.excalidraw]]

#### 锁的推广: 分布式锁

锁是语言中的一种特性, 背后蕴含互斥的理念. 只要有这个理念, 即使没有提供锁, 我们也可以自己实现.
譬如分布式锁, 几个不同机器上的线程想要互斥的进行某种操作, 我们可以自己来实现分布式锁.
首先找一个能够进行原子读写变量的机制, 譬如在redis中设定一个key为“resource”的整数, 这个整数可以是每个线程都不同的某种id. 因为redis是个单线程的服务, 所以它会线性的处理每一个请求. 这保证了原子性.
每个线程首先尝试给resource赋值, 这里NX意思是如果resource这个key不存在, 则赋值. PX 30000是过期时间.

```
    SET resource my_unique_id NX PX 30000
```

接着线程请求resource的值, 如果跟自己的id相同, 则获得锁, 这个机制保证锁可以被同一个线程多次获取, 是可重入的. 然后可以进入临界区完成任务, 之后`del resource` 删除这个key-value pair. 如果跟自己的id不同, 则说明锁被别的线程持有, 自己要么等待, 要么返回. 这个机制不会导致死锁, 因为锁设定了过期时间.
实际工程中的分布式锁, 还要稍微复杂一点. 这里就不再展开了.

### 策略2: 发生错误时补救, Lock-free Solution

还有一个策略是发生错误时补救.
这里我们需要使用到lock的底层原语, 也就是处理器指令集提供的原子操作. 系统使用这些原子操作实现了互斥量和锁.
这些原语有三种, 任意一种都可以实现互斥量和锁, 它们分别是: test-and-set, compare-and-swap, fetch-and-add. 其中比较有名和常用的是compare-and-swap, 也会被简写成CAS. 所谓“乐观锁”或者“lock-free”的算法, 都是使用了CAS函数去实现的.
![[Think 2025-06-16 21.29.14.excalidraw]]
compare_and_swap整个操作是原子化的, 只要参数1和参数2相等, 就把参数1和参数3的值交换. 并且最终返回参数1. 通过这个函数可以实现各种乐观锁的算法和atomic的类型. 所有的pattern都像下面这样, 只要value在整个计算过程中没有发生改变, 结果就能正确覆盖到value上. 否则就重试一次. [(ABA problem)](https://en.wikipedia.org/wiki/Compare-and-swap)

```
// define value somewhere...
while true:
 origin_value = value
 new_value = calculate(origin_value)
 if compare_and_swap(value, origin_value, result):
  break
```

lock的概念讲完. 现在我们来到让线程协同工作的condition variable.

## 线程协同工作

首先condition variable是用来协同两个互相配合的线程, 让线程可以被挂起或恢复运行. 通过condition variable我们也可以在共享内存模型中(艰难的)实现流水线.

### Condition Variable为何臭名昭著

condition variable臭名昭著, 这个概念难以理解.
首先这个概念的命名非常具有迷惑性, 为什么一个variable可以控制线程的挂起和恢复?  condition的意思是它和判断有关系吗?
另外这个概念在使用上有诸多隐藏条件, 首先使用condition variable必须同时使用到锁. 而condition variable的挂起和恢复也会隐式的释放和获取锁.

### 如何使用condition Variable

我们用一个例子说明condition variable的概念和使用细则.
原则上, 我们使用condition variable的场景是, 多个线程根据同一组共享变量是否满足一定条件, 来决定自己是挂起, 还是继续运行.
![[Pasted image 20250604214610.png]]
首先condition variable一定要和一个具体的锁关联. 因为它需要隐式的操作锁. 所以它的声明要么需要传入一个锁, 要么通过锁的方法进行创建. 我们用这个锁来保护共享的数据, 确保每次只有一个线程能够访问共享数据.
而condition variable名字很糟糕, 因为它并不是一个变量, 而是一个线程队列.
condition variable有两组方法: await和signal. await挂起当前线程, signal唤醒其他线程. 无论await或signal都需要在获取锁之后才能调用.
每当它调用await方法, 则做以下三件事:

- 把当前线程加入队列
- 释放锁
- 挂起当前线程.

每当它调用signal方法时, 做两件事

- 从队列中弹出一个线程唤醒. 如果使用signalAll方法, 则弹出所有线程唤醒. 这里的唤醒是把线程状态置为runnable.
- 醒来的线程会尝试获取锁. 一旦获得锁, 就从await之后的语句开始运行, 否则就等待直到获取锁为止.
 	- 获取锁从await开始运行时, 很可能运行条件已经不再满足了. 你想五点冲到食堂吃完饭, 但可能有人四点五十九冲到食堂把菜倒了. 一旦运行条件不再满足, 需要再一次await加入队列. 所以我们这里使用while语句进行循环. 一个线程如果倒霉, 有可能会反反复复唤醒, 条件不满足, 睡眠, 唤醒, 条件不满足, 睡眠.

想深入了解其机制强烈推荐《Operating Systems Three Easy Pieces》这本书的第30章.
![[Think 2025-06-04 22.07.42.excalidraw]]

c++11中的condition variable把await(c++中是wait)方法改成了cv.wait(lock, function)
一旦function返回false, 就自动再次wait. 这个改进去掉了莫名其妙的while循环, 我觉得改的很妙.
![[Pasted image 20250604223549.png]]

condition variable可以被用来实现一些高级线程同步工具. 譬如
wait-group, 或者在java中叫count down latch, 能够挂起主线程, 等到一组工作线程完成后才继续主线程.
cyclic barrier能够让一组线程互相等待, 最后同时冲线.
![[Think 2025-06-16 21.37.56.excalidraw]]

## 什么时候用stateful Concurrency Model

说了这么多, 我们什么时候使用stateful concurrency(共享内存模型), 它和之前提到的CSP模型有什么区别?
之前也说过, CSP模型适用用来实现不同种类线程之间协同工作的场景. 而共享内存模型的甜蜜点是实现同种线程竞争工作的场景, 主要是为了加速, 而不是协同. 虽然condition variable也能够让线程协同工作, 不过比起CSP模型, 还是麻烦许多.
![[Think 2025-06-15 15.44.59.excalidraw]]

## 怎么用好stateful Concurrency Model

怎么才能用好共享内存模型? 我说一点经验之谈.

- 首先业务刚开始起步, 不要盲目使用. 等有需要才引入多线程加速.
- 最好不要把线程的操作混入业务逻辑中. 两者的关注点不同, 应该分离.
- 尽量使用高级api, 譬如线程池, wait-group, cyclic barrier等等. 除非万不得已, 身不由己.
- 优化锁性能时, 我们总是尽可能减小锁的粒度. 对读多写少的场景进行优化, 譬如改用读写锁, 或者采用lock-free的解决方案.

这里因为篇幅, 就不再展开了.
