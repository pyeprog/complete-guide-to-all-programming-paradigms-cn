# 逻辑编程模型

{abbr}`逻辑编程模型(Logic Programming model)`同样属于声明式范畴，但与普通的declarative model不同，它引入了一种完全不同的编码范式。

逻辑编程模型的`核心目标是在一个搜索空间(计算空间/数据空间)中，找到满足给定约束条件的一组数据`。

:::{figure} ../material/detective-conan.jpg
例如，假设有若干件衣服、裤子及其他装饰品，需搜索（衣服, 裤子, 装饰）的元组，约束条件为不能出现红配蓝，且不能同时出现长袖、短裤和领结，目标是得到所有可能的搭配😅。
:::

在逻辑编程模型中，我们`只需指定搜索空间、约束条件和目标`，具体的搜索与回溯一般由内置的推理引擎(inference engine)执行。

此外，还有一种类似的模型称为{abbr}`关系模型(relational model)`，两者核心均为指定约束条件，在给定搜索空间中进行搜索。不同之处在于，`关系模型侧重于数据管理与查询`，常见于数据库领域；`而逻辑编程模型更关注逻辑推理`，相较关系模型更为通用。{underline}`鉴于两者内在逻辑相近，后续内容中不再特别区分`。

:::{hint}logic programming模型需要三个核心功能
1. 一种描述搜索空间的方式
2. 一种设定约束条件的方式
3. 一种求解的方式
:::

## Oz2中的relational Model

{ref}`Oz2<https://en.wikipedia.org/wiki/Oz_(programming_language>` 为了支持relational model, 引入了以下三种特性.

- choice用来指定一个变量或一组变量能够取的值, 即搜索空间. 这个例子中Shirt, Pants, Socks为三个变量, 而我们用`choice`定义了搜索空间.
- 设定约束可以通过显式使用fail, 或者直接报错来设定. 例子中使用`fail`设定了Shirt和Socks的颜色不能相同. 
- 最终我们调用内置的`SolveAll`函数来得到所有满足约束的数据tuple.

```{code} oz
:linenos:
:filename: logic_programming.oz
:emphasize-lines: 3-4,10-11,17-19,29,34
:caption: Oz2中搜索穿搭组合的例子

fun {Soft} 
    % choice代表返回值要么是beige, 要么是coral
    choice beige 
        [] coral
    end
end

fun {Hard}
    % 同理
    choice mauve
        [] ochre
    end
end

proc {Contrast C1 C2}
    % 代表C1, C2的可选范围
    choice C1 = {Soft} C2 = {Hard}
       []  C1 = {Hard} C2 = {Soft}
    end
end

fun {Suit}
    Shirt Pants Socks
in
    % 定义了搜索空间
    {Contrast Shirt Pants}
    {Contrast Pants Socks}
    % 这里使用fail, 显式对搜索进行剪枝
    if Shirt == Socks then fail end
    suit(Shirt Pants Socks)
end

% 调用SolveAll进行求解
{Browse {SolveAll Suit}}
```

:::{figure} ../material/searching-tree.png
本质上Oz2中的执行会形成一颗搜索树, 从根节点开始, 依次搜索Shirt, Pants, Socks的可能值, 遇到fail就回溯. 直到遍历整棵树, 得到所有的可行解.
:::

这里问题建模的方式, 和搜索的先后顺序会影响执行效率, 但不影响正确性, 所以这里就不再展开.

## Sql中的relational Model

Sql支持relational model, 可以对同一个问题进行建模. 同样的问题在sql中是这样的.


```{code} sql
:linenos:
:filename: query_suit.sql
:emphasize-lines: 13-16,18-23,25-38
:caption: 可以看出Sql中也有描述搜索空间, 指定约束条件和SolveAll. 只不过相比于Oz2, Sql更适合用来检索大量结构化数据. 而Oz2更适合用来建模一些组合问题. 

-- 准备数据
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

{ref}`Prolog(Programming in Logic)<https://en.wikipedia.org/wiki/Prolog>`是一种基于{abbr}`逻辑编程(logic programming)`的声明式编程语言。Prolog诞生于上世纪70年代, 并一直`作为逻辑编程和关系模型的标杆`而存在. 和其他声明式语言一样, prolog也通过描述"**what**"而不是"how"来解决问题.

关于prolog的语法可以参考这篇[cheatsheet](https://learnxinyminutes.com/prolog/).

其基本构成要素有：
• **事实（Facts）**：描述确定的关系，如 `parent(tom, bob).`, `parent(alice, tom).`
• **规则（Rules）**：定义推理逻辑，如 `grandparent(X,Z) :- parent(X,Y), parent(Y,Z).`
• **查询（Queries）**：提出问题，如 `?- grandparent(alice, bob).`

- `.`结尾代表语句结束. 
- `:-`代表后续语句定义前面的predicate. 
- `;`代表or, `,`代表and. 
- 大写字母开头代表变量. 

Prolog有一个代表性的feature, 叫做unification. 即predicate(类似于函数)既能判定真假, 也能够用来求变量的可能值, 它代表一种逻辑关系. 

```{code} prolog
:linenos:
:caption: append(M,N,L)代表三个list: M,N,L之间的关系, M+N==L
append([1, 2], [3, 4], [1, 2, 3, 4])        % True
append([1, 2], [5], L)                      % L == [1, 2, 5] 
append(L, [3, 4], [1, 2, 3, 4])             % L == [1, 2]
append([1, 2, 3], M, [1, 2, 3, 4])          % M = [4]
append([1, 2], [3], N)                      % N = [1, 2, 3]
append(P, Q, [1,2,3])                       % P = [] Q = [1,2,3]; P = [1] Q = [2, 3]; ...
```

譬如在上述例子中, append(M,N,L)
- 可以给定 M, N, L, 判定关系是否成立
- 可以给定 M, N, 计算L
- 可以给定 N, L, 计算M
- 甚至可以给定 L, 计算所有(M, N)的可能性

我们试着在prolog中, 重新实现一遍上述求穿搭的例子

```{code} prolog
:linenos:
:suit.pl

% 定义soft colors
soft_color(beige).
soft_color(coral).

% 定义hard colors
hard_color(mauve).
hard_color(ochre).

% 定义判定不同种类的颜色的predicate
different_color_types(Color1, Color2) :-
    (soft_color(Color1), hard_color(Color2));
    (hard_color(Color1), soft_color(Color2)).

% 定义判断不同颜色的predicate
different_colors(Color1, Color2) :-
    Color1 \= Color2.

% Main predicate
valid_combination(Shirt, Pants, Socks) :-
    % 设定搜索空间
    (soft_color(Shirt); hard_color(Shirt)),
    (soft_color(Pants); hard_color(Pants)),
    (soft_color(Socks); hard_color(Socks)),

    % 设定约束
    different_color_types(Shirt, Pants),    % Constraint 1
    different_color_types(Pants, Socks),    % Constraint 2
    different_colors(Shirt, Socks).         % Constraint 3

% 求解
find_all_combinations :-
    findall([Shirt, Pants, Socks], 
            valid_combination(Shirt, Pants, Socks), 
            Solutions),
    write('All valid color combinations:'), nl,
    print_solutions(Solutions).

% 定义打印结果的predicate
print_solutions([]).
print_solutions([[Shirt, Pants, Socks]|Rest]) :-
    format('Shirt: ~w, Pants: ~w, Socks: ~w~n', [Shirt, Pants, Socks]),
    print_solutions(Rest).
.
```

Prolog是一门有趣且实用的语言，曾在人工智能、专家系统、自然语言处理、数据库查询和符号推理等领域取得出色表现，值得深入了解。

## 什么时候使用logic Programming Model?

毫无疑问，在`解决搜索问题时，使用逻辑编程模型是最合适的`。虽然该模型也能用于编写通用代码，但这并非其设计初衷。

目前原生直接支持逻辑变成或关系模型的语言并不多，但主流语言通常会提供相关的三方包或库，例如Python中的[kanren](https://github.com/pythological/kanren)、Java中的[LogicNG](https://www.logicng.org/)等等.

在业务中遇到搜索问题时，可以尝试采用该模型, 而对于大量结构化数据的查询，则应优先使用数据库及SQL(或其封装)。
