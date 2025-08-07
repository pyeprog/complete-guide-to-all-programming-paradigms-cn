# Core

## 基本概念

core代表一些所有语言几乎共有的基本概念.换言之, 学习任何一门语言都可以先从这些基础元素入手.这些概念包括:

```{mermaid}
flowchart LR
    A(数据类型) --> B
    B(变量) --> C
    C(函数) --> D
    D(操作符) --> E(表达式)
```

这5个概念层层递进, 有了它们就有了程序的本体. 许多语言还包含关键词, 语句以及更多其他概念.

```{code} rust
:linenos:
:filename: primeNum.rs

// 这个例子中, 数据类型, 变量, 函数, 操作符和表达式组成了整个实现
fn is_prime_recursive(n: u32, divisor: u32) -> bool {
    if n < 2 { false }
    else if divisor * divisor > n { true }
    else if n % divisor == 0 { false }
    else { is_prime_recursive(n, divisor + 1) }
}
```

## 数据类型

数据和类型是语言最基础的拼图.类型大致分为基础类型和组合类型, 这几乎是所有语言共有的.先说基础类型: 

### 基础类型

- `数字类型`, 包括整数和浮点数.一些语言会在此基础上细分, 提供不同范围的整数和不同精度的浮点数.
- `string类型`, 是所有字符运算的基础.单个字符可视为长度为1的字符串.一些语言为字符设有单独类型, 例如C语言中的char(ASCII), Go语言中的rune.
- `symbol类型`, 在一些语言中也称为atom.你可以将它们理解为枚举(enum).symbol类型是十分重要的基础类型! [wiki中的定义](https://en.wikipedia.org/wiki/Symbol_(programming))
- `函数类型`, 通常由参数类型和返回值类型的组合表示, 例如`(u32, u32)->bool`.具体函数则是该函数类型的实例.
- 其他类型, 常见的包括boolean类型(bool运算的基础)和byte类型(位运算与内存操作的基础).

#### 关于symbol类型的例子

在下面的C++例子中, 首先定义了Color这个enum类型, 使用时调用其中具体的枚举对象.另一些语言支持更灵活的定义, 可以在任何地方直接使用symbol, 譬如在lisp中symbol无需预先定义, 可以直接使用.

```{code} cpp
:linenos:
:filename: enum.cpp
:emphasize-lines: 4,5,6,9
# include <iostream>

// define enum explicitly and group them into a enum type Color
enum Color {
    RED, GREEN, BLUE
};

int main() {
    Color c = Color::RED;  // ref to Color
    if (c == Color::RED) {
        std::cout << "C++: The Color is  " << c << std::endl;
    }
    return 0;
}
```

```{code} lisp
:linenos:
:filename: symbol.lisp
:emphasize-lines: 2,3,4

(defun main ()
    ; define symbol 'red on the fly
    (let ((c 'red))
        (if (eql c 'red)
            (format t "lisp: The Color is ~A~%" c)
            nil))
```

### 组合类型

#### tuple

组合类型中最重要的是tuple.他把若干种相同或不同类型的数据组织在一起. 譬如`(5, 10.0, "John")`就是一个`(int, float, string)`类型的tuple. tuple是非常重要, 并被广泛使用的组合类型, 譬如

- tuple可以表示unit type[^unit-type], 通常写作`()`, 即无数据的tuple
- tuple可以用来实现复杂的数据容器, 譬如array, list和map, 即tuple可以用来实现{abbr}`ADT(Abstract Data Type, 抽象数据类型, array, list, map, stack, queue等都是ADT)`.
  - array是元素数据类型统一的tuple
  - list是一个链表[^linked-list], 链表中每个结点都是一个{abbr}`2值tuple(有两个数值元素的tuple)`, 只不过其第二个值是指向下一个节点的指针
  - map是一个类型为`((key-type, value-type), ...)`的tuple

- tuple经常被用作函数参数或返回值
  - 作为返回值时经常用来感知操作是否成功, 譬如`fn() -> (value_type, err_type)`

- 很多语言都有针对tuple的{abbr}`destructuring(数据解包)`操作
  - `[head | rest_elements] = tuple`
  - `(val_a, val_b, val_c) = tuple-3`

#### 其他ADT

抽象数据类型(Abstract Data Type, ADT)是指从逻辑上定义数据及其操作的一种模型, 不关注具体实现.常见的抽象数据类型包括: 

| 抽象数据类型    | 简要说明                           |
| --------------- | ---------------------------------- |
| List(列表)      | 有序元素集合, 支持插入, 删除等操作 |
| Stack(栈)       | 后进先出(LIFO)结构                 |
| Queue(队列)     | 先进先出(FIFO)结构                 |
| Deque(双端队列) | 两端都可插入和删除的队列           |
| Set(集合)       | 无序不重复元素集合                 |
| Map(映射)       | 键值对集合, 支持通过键访问值       |
| Graph(图)       | 节点和边的集合, 表示关系网络       |
| Tree(树)        | 层次结构的节点集合                 |

这些ADT定义了数据的行为和操作接口, 具体实现可以有多种方式.

### 其他类型

当然, 类型远不止上述这些, 不同领域会有特定类型, 如计算领域的复数和矩阵等, 此处暂不展开.

## 变量

有了类型, 就有该类型的值, 自然也需要变量来承载这些值.不同语言的变量声明方式各异.

### 声明与赋值是否分开

在一些风格中赋值即声明, 另一些则区分声明与赋值.

```{code} go
:linenos:
:filename: variable.go

// separate variable declaration and assignment
var variable1 int
variable1 = 5

// assignment is the declaration
variable2 := 5
```

### 变量的可变性

变量的可变性指的是变量所存储的值是否可以在程序执行过程中被修改, `可变性是变量最重要的属性之一`.根据可变性, 变量主要分为两类: 

| 类型       | 说明                                                                |
| ---------- | ------------------------------------------------------------------- |
| 可变变量   | 变量的值可以被改变, 常见于大多数编程语言中的普通变量.               |
| 不可变变量 | 变量的值一旦赋值后不可更改, 常用于函数式编程和某些语言中的常量定义. |

其影响与意义在于:

- **可变变量**: 便于状态管理和数据更新, 并提升计算性能, 但可能引起副作用和并发问题.  
- **不可变变量**: 有助于保证数据安全和程序的可预测性, 便于调试和并发编程, 但可能会导致代码冗长或性能问题.

不同编程范式和语言对变量可变性的支持和强调程度不同.

## 函数

函数本身也是一种变量.\
对变量调用函数会返回值, 操作符则是函数调用的一种语法糖, 是函数的一种简化和符号化表现形式.例如`Add(a, b)`和`a + b`等价, 即每个操作符背后都对应一个函数. \
但操作符写法更直观, 更易于组合表达式. \
为了方便组合操作符, 必须引入操作符之间的优先级, 譬如`*`就优先于`+`.

## {abbr}`表达式(expression)`

变量, 函数和操作符共同构成表达式, 表达式可以计算出一个值.到表达式为止, 是一般语言共有的特性.

| 组成部分 | 说明                   | 例子             | 计算过程及结果                                |
| :------- | :--------------------- | :--------------- | :-------------------------------------------- |
| 变量     | 存储数据的符号名称     | `x = 5`          | 变量 `x` 的值是 5                             |
| 函数     | 接受参数并返回结果     | `f(y) = y + 3`   | 输入 `y=2`, `f(2) = 5`                        |
| 操作符   | 用于运算的符号         | `+`, `*`, `-` 等 | `3 + 4 = 7`                                   |
| 表达式   | 变量, 函数和操作符组合 | `f(x) * 2 + 1`   | 代入 `x=5`, `f(5)=8`, 计算 `(8 * 2) + 1 = 17` |

### 具体例子

```{code} python
:linenos:
:filename: expr.py

x = 5                     # 变量
def f(y):                 # 函数
    return y + 3

result = f(x) * 2 + 1     # 表达式: 调用函数 + 操作符计算
print(result)             # 输出 17
```

这个表达式由变量 `x`, 函数 `f` 和操作符 `*`, `+` 共同构成, 最终计算出一个值 17.

## {abbr}`语句(statement)`

语句不是所有语言共有的概念. 但大多数语言都会在表达式基础上引入各种语法关键词以组成语句, 进而通过表达式和语句的堆叠与嵌套来定义函数.

```{code} python
:linenos:
:filename: statement.py

def increment(x):      # 函数定义(语句)
    x = x + 1          # 赋值语句, 包含表达式 x + 1
    return x           # 返回语句, 表达式 x 的值
```

## {abbr}`IO(Input & Output)`

所有编程语言共有的另一个重要元素是与外界进行通信的输入输出(IO)机制.\
通常, 这些功能由语言自身的标准库提供, 涵盖了诸如读取和写入文件, 在屏幕上打印信息, 以及发送和接收网络请求等操作.\
没有这些IO操作, 程序就像在真空中静默运行, 执行过程完全没有任何外部反馈. \
`正因为如此, IO成为程序与外部世界交互的桥梁, 使得程序的执行结果能够被观察, 验证和利用, 并产生实际的影响和价值`.

---

后续所有模型都会基于以上这些概念和能力展开.

---

[^unit-type]: Unit 类型(单位类型)是只有一个值的类型.它用来表示没有有意义的信息, 类似于某些语言中的 void, 但与 void 不同的是, 单位类型是一个真正的类型, 且只有一个值.
    关于单位类型的关键点: 
    - 唯一值: 通常写作 ()(读作“单位”).
    - 用途: 表示函数或表达式没有返回有意义的值, 但仍然返回一个值
    - 使用场景
      - 执行副作用但不返回有用数据的函数
      - 需要类型但不需要数据的占位符.

[^linked-list]: 在很多函数式或声明式语言中, list都是链表. 其实现为
    ```{mermaid}
    graph TD
      A_val["1"] 
      B_val["2"]
      C_val["3"]
      D_val["null"]

      A --> A_val
      B --> B_val
      C --> C_val
      D --> D_val

      A["(value, next)"] --> B["(value, next)"]
      B --> C["(value, next)"]
      C --> D["(value, null)"]

    ```