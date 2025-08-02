# Constraint Programming Model

![[Think 2025-06-24 11.56.34.excalidraw]]
Constraint Programming model是一类特殊的logic programming model.
相比于logic programming Model, Constraint Programming Model的搜索空间是连续的数值空间. 其约束的形式是一组公示. 而最终求解的目标是求得最优解.

| Logic Programming Model | Constraint Programming Model |
| ----------------------- | ---------------------------- |
| 搜索空间是离散的                | 搜索空间是连续的数值空间                 |
| 约束是boolean expression   | 约束是equation                  |
| 求可行解                    | 求最优解                         |
| 搜索问题                    | 规划问题(譬如线性规划)                 |

因为这两个模型如此相似, 所以Constraint Programming Model的核心功能也是

1. 一种描述数值空间的方式
2. 一种设定约束条件的方式
3. 一种求解的方式

只不过提供了不同的语法. 譬如在Oz2中, 求两个数之积得到一个回文数, 代码如下.
![[Pasted image 20250624120003.png]]

Constraint Programming Model相比于Relational Model, 提供了更丰富的求解算法和策略. 它甚至可以根据已有的约束条件推理出新的约束条件. 这里就不再详细说明了.

Constraint Programming适用于各种规划问题. 通常语言不会直接支持这个模型. 而是会以library或package的方式提供类似的能力. 譬如python中的pyomo提供了线性规划相关的实现, 其使用方式非常类似于刚才的例子.

使用Constraint Programming Model最困难的点在于建模和优化. 通常每个业务问题分析角度不同, 建模也大不相同. 而优化更是需要耐心调试. 这个模型不太能够用在需要实时响应的系统中.
