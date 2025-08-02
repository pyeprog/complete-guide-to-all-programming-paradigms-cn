# Intro

## 前言

本书尝试带你概览绝大部分主流编程语言的`重要特性`以及这些特性对应语言`背后的模型`.
了解这些模型和对应的特性能够快速了解这门语言`能做什么`, 以及`怎么做`.

:::{figure} ../material/minecraft-torch.webp
掌握了这些语言模型,就像在黑暗中点亮一盏盏`火把🕯️`. 当你清晰看到编程语言的全貌和边界, 你会获得安全感和自信.\
以后即使你面对全新的语言和突破性的特性, 你也能迅速定位它们在整个领域中的位置.\
这样一来, `语言本身的复杂性就不再是障碍了, 你的思考空间将变得纯净, 更能够直击问题的本质`.
:::

## 目标读者

:::{important} Notice
这本书的主题{underline}`不是`从零开始学习一门语言，而是一次性理解多种语言。因此，{underline}`读者需要至少掌握一门编程语言`，了解一定的并发知识，并且最好具备一定的实战经验。
:::

如果你是完全的新手，想要入门，那么观看完这个视频后你可能会发现，我在用一些陌生的概念解释另一些陌生概念，这对入门学习并不利。`对于学习而言，内容的选择非常重要`.

:::{figure} ../material/stephen-krashen.jpg
:alt: Stephen Krashen
:align: center
:width: 100%
语言学家Stephen Krashen认为学习一门语言需要可理解的内容, [参考视频](https://www.bilibili.com/video/BV1wx4y1o7Po)
:::

:::{figure} ../material/chants-of-sennaar.png
:alt: chants of sennaar
:align: center
:width: 100%
如果你曾经玩过[巴别塔圣歌](https://store.steampowered.com/app/1931770/_/?l=schinese)这款游戏，可能会对此有更深的体会。
:::

对于新手来说，学习语言本身只是第一步，更重要的是学会如何使用语言进行实战。对于完全没有编程基础的朋友，我推荐《笨办法学Python3》(a.k.a learn python the hard way)这本入门书，[这里](https://learnpythonthehardway.org/python3/)是在线英文版。

::::{grid} 2
:::{image} ../material/learn-python-the-hard-way.jpg
:width: 50%
:::

:::{image} ../material/learn-python-the-hard-way-cn.jpg
:width: 50%
:::
::::

## 模型树

使用编程语言的本质目的是生产和创造。了解多种语言意味着你的创造范围不仅局限于某一种应用。语言能够作为桥梁，贯通不同计算机科学分支中的概念，加深对不同抽象范畴的理解。

:::{figure} ../material/model-tree.png
:align: center
:label: intro:model-tree
模型树
:::

所有语言都开始于declarative model声明式模型, 从它延伸出4个分支, 分别是面向并发模型, 显式状态及其并发模型, 函数式模型和逻辑编程模型. 元编程独立于这个体系. 其中

- **Core**是所有语言共有的元素.
- **Declarative model**是一个不包含"_变量_"和循环的简单编程模型, 掌握这种模型能锻炼编写算法的能力.
- **Concurrent declarative model**及其后续模型, 在Declarative model的基础上加入了线程, 线程间通信, 并最终发展为面向并发编程.
- **Explicit state model**引入了_变量_和循环, 它把显式可变状态和状态的操作引入到代码中, 大大增强了代码的表现力.
- **Stateful concurrency**等模型在可变状态的前提下引入了并发机制, 包括lock, condition variable, coroutine和async.
- **Modular model**, **object based**和**object oriented model**是我们日常编码的默认模型, 深入理解它们能让你更好的组织项目, 写出漂亮的实现.
- **Functional model**揭示了一些函数式编程的概念, 譬如high order function, curry, monad以及enum data type.
- **logic programming**和**constraint programming**提供搜索问题和规划问题的一般解法.
- **Meta programming**介绍了全部的元编程技巧, 包括macro, compile time compute, reflection, meta-data等等.

## 语言模型的发展方向

语言模型的发展总体呈现两个自然趋势。

### 趋势一：由顺序到并发

语言模型最初以顺序执行为主，这是计算机架构的本质属性所决定的，因此早期的编程语言与此高度契合。但现实世界中万物本质上是并发的。为了模拟复杂的真实环境，几乎所有现代语言在不同程度上都支持并发。

### 趋势二：由简到繁  

第二个趋势是语言特性由简到繁。这里的“简”与“繁”指的是语言中概念和特性的多少，直观表现为关键词数量、支持的开发范式种类及语言的复杂程度。即使是同一门语言，早期版本通常也比当前版本更为简洁，例如ANSI C与现今的C99版本，后者引入了更多新概念。

```c
#include <stdio.h>

int main() {
    int x = 5;
    int array[x];  // Allowed in C99: size is variable, not in Ansi C
}
```

## 双刃剑

然而，语言的表现力是一把双刃剑。

- 特性越多，表现力越强，实现复杂算法越简洁，但理解难度也随之增加，滥用的风险也更大。
- 反之，表现力较弱时，编写复杂算法较为冗长，但理解相对容易。

这是一个客观规律. 因此语言并不是越复杂越好, 也不是越简单越好. 我们在选择时内心需要有一个准则, 这个后文会介绍.

---

接下来我会按照脉络来介绍每一个模型的概念, 适用范围和实践经验.
