# Message Passing Model

上面提到的concurrent declarative model线程之间无法交换数据, 为了解决这个问题, Hoare在1978年的论文中引入了“Communicating sequential process"模型, 简称CSP模型. 因为它靠线程之间传递消息的机制来解决并发中的问题, 我们也称之为message-passing model. 我们不再说明早年的模型是什么样子, 只说明当下它最流行的形态: channel, 并以go中的channel作为范本进行说明. 下面的内容中, 我们不加区分的使用goroutine和线程这两个名词.

## CSP Model带来的新特性

message-passing model在concurrent declarative model之上增加了两个新特性. channel和select.

### Channel

channel行为上类似一个AtomicQueue, 你可以把数据对象塞入channel, 也可以从channel中提数据出来. 从对象的角度去理解, 它是一个一等公民对象, 可以被传递到程序的每个角落, 塞到容器里, 甚至把它放入另一个channel中, 并且不用考虑“复制”它的开销.
[![How Does Golang Channel Works. Understanding Inner workings of the… | by  Jerry An | Level Up Coding](https://miro.medium.com/v2/resize:fit:1002/1*TwLvjm5ivaQKtYA3HbdmMw.png)

channel有几个主要特性.
第一, 无论读写都是原子化的, 所以不必担心数据竞争, 数据的读写都是“顺序的”(sequential).
第二, channel有容量, 容量本身意味着有多少message能被channel缓存.
第三, channel可以被关闭. 关闭一个channel代表着线程想要结束通信. 关闭的channel不能写, 只能读. channel用到一半关闭, 其中数据也不会丢失, 而是可以原样读出, 数据读完了, 再读就是类型的默认值, 譬如int类型, 读出0.
第四, channel可以控制线程的挂起和恢复. 从空的channel中取数据会挂起线程, 等到channel中有数据则恢复运行. 同理写一个满的channel也会挂起线程, 等到channel有空间时则恢复运行. 比较特殊的是对于容量为0的channel, 任何写入都会挂起, 任何读取也会挂起, 只有读写双方都存在时, 才能交换数据, 这能够同步两个线程的读写.

设想两个线程启动时持有同一个channel. 一个线程往里写, 一个线程往外读. 这样就自然达成了数据传递的作用, 如此一来还没有竞态条件, 所以不会导致数据错误等问题.

### Select

第二个特性select, select是一个关键词, 其灵感来自操作系统的IO多路复用. 它能够并联若干条channel. 一旦任意一条能够被读出, 或者被写入, 就会进入相应的分支中执行相应的代码, 如果没有任何可操作的channel, 它就会挂起或者执行默认操作. 这个特性很强, 他可以让每个线程都化身为一个迷你服务, 提供监听, 线程管理, 流水线聚合等能力.
[![Go: Ordering in Select Statements | by Vincent | A Journey With Go | Medium](https://miro.medium.com/v2/resize:fit:1400/1*pBaarfv1zk9JIeER9jsWrQ.png)

## 怎么使用Channel和Select

这两个概念不难理解, 但在实战中channel和select怎么用?

首先说说怎么用, channel和select除了零碎的单独使用之外, 还有几个经典的使用模式.
首先是创建线程(这里是goroutine)的经典模式.
![[Think 2025-05-29 16.04.37.excalidraw]]
第一, 在大部份应用中, goroutine创建之后, 总会通过channel传出自己计算后的结果. 谁来负责管理这些channel呢, 或者换句话说, 在计算完毕后谁来关闭这些channel?
我们总是认为哪个goroutine给channel提供数据, channel就归谁管理. 所以我们把创建channel, 创建goroutine封装在一起, 如果goroutine结束, channel也会被关闭.
这种写法就是经典的写法.

第二, 创建的goroutine, 我们几乎总是想要能够控制它. channel除了用来传输数据之外, 我们也可以用来传输控制信号. 只需要我们用select把数据和控制的channel并连起来. 就像例子中, 我们在其他线程, 一旦给done channel传任何一个值或者关闭done channel, 都会让这个goroutine退出.

## What to Build?

接着, 我们用它构建什么呢?
比较常见的两种场景, 第一种是构建流水线pipeline.
如果我们把一个计算拆成若干步骤, 每一个步骤写成一个函数, 并放入goroutine中不断循环运行. 数据从传入一个goroutine然后把结果输出传给另一个goroutine, 这样我们就组成了一个流水线.

每个step可以串联在一起, 甚至可以fan out一对多, 或者fan in多聚一. 以此来组建更加复杂的流水线.
![[Think 2025-05-29 22.35.40.excalidraw]]
![[Think 2025-06-15 20.23.54.excalidraw]]

第二个场景是goroutine之间的管理, 譬如总有一些goroutine会因为各种原因报错关闭. 此时我们需要supervisor goroutine来管理其他的worker goroutine, 监听它们是否还存活, 如果失活了, 需要由它来重启这些worker goroutine.
![[Think 2025-06-15 20.36.39.excalidraw]]
每个worker需要额外返回一个心跳channel, 并且隔一段时间发一次心跳. supervisor中设定计时器, 只要在计时器结束前收到心跳, 就认为worker一切正常, 于是重置计时器, 反之就关闭旧worker, 启动新worker.
