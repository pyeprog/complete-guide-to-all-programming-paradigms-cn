# 异步(Async)

我们之所以很少自己实现协程库, 是因为实现后往往发现, 只不过是做了一版不够完善的async特性. 那么, 什么是async呢? 

Async是语言为支持异步IO而设计的一套协程调度机制, 目标是提高单线程IO效率和吞吐量. 相比原始协程, 它更符合人体工学. 

:::{image} ../material/async-speed-diagram.png
:::

## Async 提供的新特性

async 在语言中引入两个核心概念:   

-  一组关键词 `async` 和 `await`, 使用它们可以更好地定义协程及协程之间的调度.   
-  一个{abbr}`协程队列(事件队列)`, 所有被挂起的协程会进入该队列, 待可运行时则出队执行. JavaScript中该队列隐式存在, 其他语言则需显式定义.   

:::::{tab-set}

::::{tab-item} javascript
```{code} javascript
:linenos:
:emphasize-lines: 2,3

async function fetchData(url) {
  const response = await fetch(url);
  const data = await response.text();
  console.log(data);
}
fetchData('https://example.com');
```
::::

::::{tab-item} python
```{code} python
:linenos:
:emphasize-lines: 5-7

import asyncio
import aiohttp

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.text()
            print(data)

# 隐式定义了协程队列, 并把fetch_data对应的协程加入其中并执行
asyncio.run(fetch_data('https://example.com'))
```
::::

::::{tab-item} rust

```{code} rust
:linenos:
:emphasize-lines: 5,6

use async_std::task;
use surf;

async fn fetch_data(url: &str) -> Result<(), surf::Exception> {
    let mut res = surf::get(url).await?;
    let body = res.body_string().await?;
    println!("{}", body);
    Ok(())
}

fn main() {
    task::block_on(fetch_data("https://example.com")).unwrap();
}
```
::::

:::::

在使用上

-  async 关键词置于函数定义前, 声明该函数为async function. 调用async function 会返回一个coroutine.   
-  在异步函数调用前加await, 表示被调用协程开始执行, 而当前协程挂起并加入队列. 参考[async/await 工作原理](https://devblogs.microsoft.com/dotnet/how-async-await-really-works/#async/await-under-the-covers). 当被调用协程完成后, 当前协程被唤醒, 检测await任务状态完成, 则继续执行后续代码. 

async特性易于理解, 使用时无需深入了解其底层原理. 不同语言实现细节不同, 此处不再展开. 

## 什么时候使用 async

适用于IO密集且性能关键的场景, 如大量文件读写, 大量 URL 请求, 大量 API 调用, 数据库访问等. 

## 如何实现自己的 async Function? 

语言或标准库通常内置各种async function, 如文件读写, 网络请求等. 开发者只需通过await调用这些async function, 组合实现自己的async function即可.  

开发时, 建议先实现同步版本并进行性能测试, 只有在必要时才改写为async版本. 这样更易于调试, 避免陷入过早优化的陷阱. 