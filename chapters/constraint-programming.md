# 约束编程模型

{abbr}`约束编程模型(constraint Programming model)`是一类特殊的逻辑编程模型.

简单理解的话, 相比于逻辑编程模型, [约束编程模型](https://en.wikipedia.org/wiki/Constraint_programming)的搜索空间是连续的数值空间, 其约束形式为一组方程, 最终求解目标是最优解. 

| Logic Programming Model | Constraint Programming Model |
| ----------------------- | ---------------------------- |
| 搜索空间是离散的        | 搜索空间是连续的数值空间     |
| 约束是布尔表达式        | 约束是方程                   |
| 求可行解                | 求最优解                     |
| 解决搜索问题            | 解决规划问题(如线性规划)     |

由于两者非常相似, Constraint Programming Model的核心功能也包括:

1. 描述数值空间的方式  
2. 设定约束条件的方式  
3. 求解方式  

只不过语法不同. 例如在Oz2中, 求两个数之积为回文数的代码如下: 

```{code} oz
:linenos:
:filename: palindrome_by_2_nums.oz

proc {Palindrome ?Sol}
    sol(A)=Sol
    B C X Y Z
in
    % 定义A, B, C的取值范围
    A::0#999999  B::0#999  C::0#999
    
    % 定义A, B, C之间的关系
    A=:B*C
    
    % 定义X, Y, Z的取值范围
    X::0#9  y::0#9  Z::0#9
    
    % 定义A和X, Y, Z之间的关系
    A=:X*100000 + Y*10000 + Z*1000 + Z*100 + Y*10 + X    % XYZZYX
    
    % 求解
    {FD.distribute ff [X Y Z]}
end
```

相比于逻辑编程, `约束编程模型提供了更丰富的求解算法和策略, 甚至能够根据已有约束推导出新的约束`, 细节此处不再赘述. 

约束编程模型适用于各类规划问题. 通常语言不会直接支持该模型, 而是通过库或包提供相关能力. 例如Python中的[pyomo](http://www.pyomo.org)提供线性规划实现, 使用方式类似上述例子. 

`使用约束编程最困难的部分在于建模和优化`. 每个业务问题分析角度不同, 建模方式差异较大；优化过程也需耐心调试. `该模型不太适合用于需要实时响应的系统`. 