# Logic Programming Model

![[Think 2025-06-24 11.46.25.excalidraw]]
Logic Programming model也是声明式的, 跟普通的declarative model不同, 它引入了一种完全不同的编码范式.

logic programming model的核心目标是在一个搜索空间(计算空间/数据空间)中, 搜索到一组数据, 而这组数据需要满足给定的约束条件. 譬如, 我有若干件衣服, 若干条裤子以及其他装饰, 我需要搜索(衣服, 裤子, 装饰)的tuple, 给定约束条件是, 不能出现红配蓝, 且不能出现长袖, 短裤和领结, 目标是得到全部可能的搭配.
![[Pasted image 20250624114903.png]]

在logic programming model中, 我们只需要指定搜索空间, 约束条件和目标. 具体的搜索和回溯交给内置的inference engine去执行.

另有一种类似的model, 名为relational model, 两者的核心都是指定约束条件, 给定搜索空间中进行搜索. 不同点在于relational model关注于数据的管理和搜索, 更常见于数据库领域, 而logic programming model关注于逻辑推理, 相比于relational model更加通用. 鉴于两者都有共同的内在逻辑, 后面不会特别区分两者.

![How To Match Clothes: The BEST Clothing Color Combos for Guys](https://i.pinimg.com/736x/8d/cb/8b/8dcb8b10d5d4e6e4ecf17cf907f12ffe.jpg)
logic programming模型需要三个核心功能

1. 一种描述搜索空间的方式
2. 一种设定约束条件的方式
3. 一种求解的方式

## Oz2中的relational Model

Oz2为了支持relational model, 引入了以下三种特性.

- choice用来指定一个变量或一组变量能够取的值, 即搜索空间. 这个例子中Shirt, Pants, Socks为三个变量, 而我们用choice指定了(Shirt, Pants)这个tuple能够取的值, 以及(Pants, Socks)能够取的值
- 设定约束可以通过显式的fail, 或者隐式的exception来设定. 例子中使用`if Shirt==Socks then fail end`设定了Shirt和Socks的颜色不能相同.
- 最终我们调用内置的SolveAll函数来得到所有满足约束的数据tuple.

以上是在Oz2这门语言中relational model的体现.
![[Pasted image 20250613115209.png]]
![[Pasted image 20250613115914.png]]
本质上Oz2中的执行会形成一颗搜索树, 从根节点开始, 依次搜索Shirt, Pants, Socks的可能值, 遇到fail就回溯. 直到遍历整棵树, 得到所有的可行解.
![[Pasted image 20250613115840.png]]

这里问题建模的方式, 和搜索的先后顺序会影响执行效率, 但不影响正确性, 所以这里就不再展开.

## Sql中的relational Model

如果在Sql中, 这是这样的体现. 可以看出Sql中也有, 描述搜索空间, 指定约束条件和SolveAll. 只不过相比于Oz2, Sql更适合用来检索大量结构化数据. 而Oz2更适合用来建模一些组合问题. 同样的问题在sql中是这样的.

```sql
-- preparation
CREATE TABLE colors (
    color_name VARCHAR(50) PRIMARY KEY,
    color_category VARCHAR(10) CHECK (color_category IN ('Hard', 'Soft'))
);

INSERT INTO colors (color_name, color_category) VALUES
('Mauve', 'Hard'),
('Ochre', 'Hard'),
('Beige', 'Soft'),
('Coral', 'Soft');

SELECT -- "solveAll"
    Shirt.color_name AS shirt_color,
    Pants.color_name AS pants_color,
    Socks.color_name AS socks_color,
    
FROM -- 指定搜索空间
    colors Shirt
CROSS JOIN 
    colors Pants
CROSS JOIN 
    colors Socks

WHERE -- 指定约束条件
    (
      (Shirt.color_category = "Soft" AND Pants.color_category = "Hard")
   OR
      (Shirt.color_category = "Hard" AND Pants.color_category = "Soft")
    )
    AND
    (
      (Pants.color_category = "Soft" AND Socks.color_category = "Hard")
      OR
      (Pants.color_category = "Hard" AND Socks.color_category = "Soft")
    )
    AND
    Shirt.color_name <> Socks.color_name
```

## Prolog中的logic Programming Model

Prolog（Programming in Logic）是一种基于逻辑编程(logic programming)的声明式编程语言。Prolog诞生于上世纪70年代, 并一直作为逻辑编程和关系模型的标杆而存在. 和其他声明式语言一样, prolog也通过描述“what”而不是“how”来解决问题.

其基本构成要素有：
• **事实（Facts）**：描述确定的关系，如 parent(tom, bob). parent(alice, tom).
• **规则（Rules）**：定义推理逻辑，如 grandparent(X,Z) :- parent(X,Y), parent(Y,Z).
• **查询（Queries）**：提出问题，如 ?- grandparent(alice, bob).

这里`.`结尾代表语句结束. `:-`代表后续语句定义前面的predicate. `;`代表or, `,`代表and. 大写字母开头代表变量. Prolog有一个代表性的feature, 叫做unification. 即predicate(类似于函数)既能判定真假, 也能够用来求变量的可能值, 它代表一种逻辑关系. 譬如这个例子.

```prolog
append([1, 2], [3, 4], [1, 2, 3, 4])  % True
append(L, [3, 4], [1, 2, 3, 4])  % L == [1, 2]
append([1, 2, 3], M, [1, 2, 3, 4])  % M = [4]
append([1, 2], [3], N)  % N = [1, 2, 3]
append(P, Q, [1,2,3])  $ P = [] Q = [1,2,3]; P = [1] Q = [2, 3]; ...
```

之前Oz2中的例子, 也可以用Prolog实现. 可以看出, 在代码结构上它们都有几分相似.

```prolog
% Define soft colors
soft_color(beige).
soft_color(coral).

% Define hard colors
hard_color(mauve).
hard_color(ochre).

% Helper predicate to check if two colors are different types
different_color_types(Color1, Color2) :-
    (soft_color(Color1), hard_color(Color2));
    (hard_color(Color1), soft_color(Color2)).

% Helper predicate to check if two colors are different
different_colors(Color1, Color2) :-
    Color1 \= Color2.

% Main predicate to find valid color combinations
valid_combination(Shirt, Pants, Socks) :-
    % Generate all possible color assignments
    (soft_color(Shirt); hard_color(Shirt)),
    (soft_color(Pants); hard_color(Pants)),
    (soft_color(Socks); hard_color(Socks)),

    % Apply constraints
    different_color_types(Shirt, Pants),    % Constraint 1
    different_color_types(Pants, Socks),    % Constraint 2
    different_colors(Shirt, Socks).         % Constraint 3

  

% Predicate to find and display all solutions
find_all_combinations :-
    findall([Shirt, Pants, Socks], 
            valid_combination(Shirt, Pants, Socks), 
            Solutions),
    write('All valid color combinations:'), nl,
    print_solutions(Solutions).

% Helper predicate to print solutions nicely

print_solutions([]).
print_solutions([[Shirt, Pants, Socks]|Rest]) :-
    format('Shirt: ~w, Pants: ~w, Socks: ~w~n', [Shirt, Pants, Socks]),
    print_solutions(Rest).
```

Prolog是一门有趣且实用的语言. 在人工智能、专家系统、自然语言处理、数据库查询和符号推理等领域有过出色表现. 值得了解一番.

## 什么时候使用logic Programming Model?

毫无疑问, 在解决搜索问题上, 使用该模型是最合适的. 虽然它也可以编写通用代码, 但那毕竟不是该模型的设计初衷.
目前支持relational model的语言不是很多, 但是主流语言一般会有支持logic / relational model的package或者library, 譬如python中的[kanren](https://github.com/pythological/kanren), java中的[LogicNG](https://www.logicng.org/)
在业务中如果遇到搜索问题, 可以尝试用这个model. 如果是大量结构化数据的查询, 则使用数据库和sql(或其封装).
