# 从modularity到OOP

在 explicit state 模型之后, 关于对象的理论逐渐兴起. 其模型, 设计范式和最佳实践在1960年之后的30年间不断被研究. 直到今天, 面向对象编程(OOP)依然是极其重要的编程范式之一.   

目前几乎所有关于对象的学习材料都是从class语法开始介绍, 随后讲解数据封装, 访问限制, 类的继承和多态机制. 这往往让人误以为“正统”的对象模型就是如此.   

:::{image} ../material/god-and-oop.png
:::

但class风格的OOP并非唯一的对象模型, 就如橘子不是唯一的水果. OOP也不是起点, 它是从更{abbr}`简单的模型(如 modular model, object-based model)`逐步发展而来. OOP也不是终点, OOP的形态不断在发展, 当其进入并发领域时, 还会演变成concurrent OOP模型. 

所有这些模型都值得逐一介绍. 原因之一是, 目前仍有许多现代语言不支持OOP, 例如 C, Elixir；还有不少语言不采用class风格OOP, 如Rust和Golang. 理解它们的设计初衷和考量非常重要. 原因之二是, 根据精益设计原则, 应选择最简单且能清晰实现功能的模型, 避免杀鸡用牛刀. 有时你并不需要 OOP, 可能只需更简单的模型即可.   


modular model是基础. 在其之上诞生了两种不同的对象编程范式: 一种是 object-based programming, 另一种是 object oriented programming, 两者设计初衷和使用模式均有显著差异. 接下来我们将依次介绍这三个模型.   