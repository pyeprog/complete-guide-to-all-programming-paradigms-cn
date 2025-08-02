# 从modularity, object-based到OOP

在explicit state模型之后, 关于对象的理论逐渐变得流行. 其模型, 设计范式, 最佳实践在1960之后的30年间不断的被研究. 直到现在面向对象编程(OOP)仍旧是极其重要的一种编程范式.
目前几乎所有关于对象的学习材料都是从class的语法开始介绍, 随后是对数据的封装, 对访问的限制, 类的继承, 多态的机制. 这会给人一种“正统”对象模型就是如此的错觉.
但class style OOP并不是唯一的对象模型, 就像橘子不是唯一的水果.
OOP并不是起点. 现在的OOP是从更简单的模型, 如modular model, object-based model逐步发展而来. OOP也并不是终点, OOP进入并发领域, 就会演变成concurrent OOP模型.
所有这些模型都值得一一介绍. 原因一是, 目前仍旧有很多现代语言, 并不支持OOP, 譬如c, elixir. 也有许多语言并不采纳class style OOP, 譬如rust和golang. 理解它们的设计初衷和考量很重要. 原因二是, 在精益设计的原则中, 我们应该使用能清晰简洁实现功能的最简单的模型, 杀鸡不用牛刀. 有时候你并不需要OOP, 可能只需要更简单的模型.

[modular model是一切的基础](https://www.youtube.com/watch?v=QyJZzq0v7Z4)(25:00). 随后object大行其道, 诞生了两种不同的object编程范式, 一种是object-based programming, 另一种就是OOP, 两者设计初衷有很大差别, 使用模式上也是. 接下来我们会依次介绍这三个模型.
![[Pasted image 20250606215124.png]]
