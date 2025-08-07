# 函数式模型

之前提到的{abbr}`声明式模型(declarative model)`中没有可变状态, 很多人将其等同于{abbr}`函数式模型(functional model)`, 但声明式模型中依然存在负责与外界IO交互的函数, 并且会使用try-catch等机制处理异常, 因此它并非纯粹的函数式模型. 

与此对应, {abbr}`纯函数式模型(pure functional model)`在声明式模型基础上, 将函数式和不可变性推向极致. 

纯函数的概念类似于数学中的函数: 给定相同输入, 总是产生相同输出, 且{abbr}`无副作用(不修改全局变量, 不进行IO操作, 不改变状态等)`. 为了让纯函数式编程实用, 必须引入IO操作. `纯函数式模型通过monad将IO, 异常等不可避免的副作用隔离开`, 实现纯粹的函数式编程, 这部分内容后续会详细介绍. 

虽然在日常工作中, 我们很少用纯函数式语言(如Haskell)来开发项目, 但其模型中的机制早已融合进几乎所有主流语言. 

- 现代语言几乎都将函数视为第一类公民, 非函数式语言也普遍拥有函数式库或包, 许多高阶函数甚至直接集成于标准库
- 纯函数式语言的`类型系统`被借鉴, 成为其他语言中的参数化枚举(parametrized enum)
- Monad被用于解决null判断和副作用处理等问题. 

因此, 纯函数式模型值得深入了解. 

:::{image} ../material/functional-programming.png
:::

## Expression First的代码风格

相比其他语言, 纯函数式语言在风格上有显著差异. 

这个例子实现一个函数, 计算及格同学的平均分, 如果无人及格则返回"No Passes".

::::{tab-set}
:::{tab-item} statement first
```{code} javascript
:linenos:
:filename: grade.js
:caption: 整个函数由若干条语句堆叠而成

function calcGrades(grades) {
    let passed = grades.filter(g => g >= 60);
    if (passed.length === 0) {
        return "No passes";
    }
    
    let sum = 0;
    for (let grade of passed) {
        sum += grade;
    }
    
    let average = sum / passed.length;
    return "Average: " + average;
}
```
:::

:::{tab-item} expression first
```{code} haskell
:linenos:
:filename: grade.hs
:caption: 整个函数由一个嵌套的表达式组成

calcGrades :: [Int] -> String
calcGrades grades =
    let passed = filter (>=60) grades
        average = sum passed / fromIntegral (length passed)
    
    in if null passed then "No passes" else "Average: " ++ show average
```
:::

::::

大多数语言的代码由{abbr}`语句(statement)`构建, `编程即堆叠计算或命令的语句`.\
而纯函数式语言中, 几乎所有元素都是{abbr}`表达式(expression)`, `编程则是嵌套组织表达式`. 且在绝大多数情况下, `纯函数式语言中函数体只有一个嵌套表达式`. 

```{code} haskell
:linenos:
:filename: single_expr.hs
:caption: 这是因为纯函数式语言中的绝大多数表达式无副作用. 若将无副作用的表达式顺序堆叠执行, 函数只能返回其中一个表达式的结果, 其余表达式即使执行, 因无副作用, 也等同于未执行.

-- 计算两个数的平方和
squareSum1 :: Int -> Int -> Int
squareSum1 x y = (x * x) + (y * y)

-- let表达式
squareSum2 :: Int -> Int -> Int
squareSum2 x y = 
  let a = x * x   -- 无副作用表达式
      b = y * y   -- 无副作用表达式
  in a + b        -- 返回结果

-- 无谓的堆叠表达式🤷
squareSum3 :: Int -> Int -> Int
squareSum3 x y = 
  x * x  -- 这个表达式无副作用, 但结果未被返回
  y * y  -- 这个表达式无副作用, 也未被返回
  (x * x) + (y * y)  -- 只有这个表达式的结果被返回
```

可以说, `只要强调无副作用, 语言基本都会偏向expression-first的代码风格`. 

其他主流语言也逐步采纳这种代码风格. 一些关键词语句被改为表达式, 诸如`if/else`, `for/loop`, `switch/match`让它们最终能计算出一个值. 这种风格极大提升了代码的表现力. 

```{code} rust
:linenos:
:filename: expr_first.rs
:emphasize-lines: 10,15-19,27

enum Color {
    Red,
    Green,
    Blue,
}

fn main() {
    let x = 5;
    // if/else 表达式返回值
    let result = if x > 10 { "大于10" } else { "小于等于10" };
    println!("结果: {}", result); // 输出: "结果: 小于等于10"
    
    let color = Color::Green;
    // match 表达式返回值
    let message = match color {
        Color::Red => "红色",
        Color::Green => "绿色",
        Color::Blue => "蓝色",
    };
    println!("颜色: {}", message); // 输出: "颜色: 绿色"

    let numbers = vec![1, 2, 3];
    let mut idx = 0;
    let mut acc = 0;

    let sum = loop {
        // break 返回loop表达式的值
        if idx >= numbers.len() { break acc; }
        acc += numbers[idx];
        idx += 1;
    };
}
```

## 高阶函数和curry函数

就像object model说一切皆对象, pure functional model说一切都是数据和函数.

函数中, `高阶函数就是我们日常使用最频繁, 最广泛的函数式元素了`. 以下是python中的一些高阶函数, 其他语言中也有类似高阶函数. 

```{code} python
:linenos:
:filename: commonly_used_high_order_func.py
:caption: 推荐[toolz](https://github.com/pytoolz/toolz)这个高阶函数库

from functools import reduce
from itertools import takewhile, dropwhile
from collections import defaultdict
from toolz import compose, memoize, groupby

# map: 对列表中的每个元素执行平方操作
mapped = list(map(lambda x: x**2, [1, 2, 3]))  # [1, 4, 9]

# filter: 筛选出列表中所有偶数
filtered = list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4]))  # [2, 4]

# reduce: 将列表元素累加起来, 初始值为0
reduced = reduce(lambda acc, x: acc + x, [1, 2, 3], 0)  # 6

# foldl(左折叠): 等价于reduce, 从左到右累加
foldl_total = reduce(lambda acc, x: acc + x, [1, 2, 3], 0)  # 6

# sort: 对列表进行排序
sorted_list = sorted([2, 3, 1, 4])  # [1, 2, 3, 4]

# forEach: 遍历列表并打印每个元素
for x in [1, 2, 3]:
    print(x)

# flatmap: 先映射再扁平化, 合并嵌套列表
lists = [[1, 2], [3, 4]]
flat = [item for sublist in lists for item in sublist]  # [1, 2, 3, 4]

# zipWith: 对应位置元素相加
pairs = [a + b for a, b in zip([1, 2, 3], [4, 5, 6])]  # [5, 7, 9]

# compose: 函数组合, 先执行div3, 再执行mul10, 最后执行add5
add5 = lambda x: x + 5
mul10 = lambda x: x * 10
div3 = lambda x: x / 3
calculate = compose(add5, mul10, div3)
result = calculate(3)  # 计算结果为15

# takeWhile: 从列表开头取出满足条件的元素
taken = list(takewhile(lambda x: x < 3, [1, 2, 3, 4]))  # [1, 2]

# dropWhile: 丢弃开头满足条件的元素, 返回剩余部分
dropped = list(dropwhile(lambda x: x < 3, [1, 2, 3, 4]))  # [3, 4]

# groupBy: 根据字符串长度分组
words = ["cat", "apple", "cherry", "dog"]
grouped = groupby(len, words)  
# 结果为 {3: ['cat', 'dog'], 5: ['apple'], 6: ['cherry']}

# memoize: 对递归函数进行缓存, 避免重复计算
@memoize
def factorial(x):
    if x <= 1:
        return 1
    return x * factorial(x - 1)

factorial_with_memo = factorial
factorial_with_memo(1000)  # 第一次计算较慢
factorial_with_memo(1000)  # 第二次调用瞬间返回, 速度极快
```

此外, 函数的柯里化(curry化)是另一个非常实用且常用的特性. 配合高阶函数使用, 能够大幅简化代码. 柯里化后的函数只有在接收到全部参数时才会被调用；如果只提供部分参数, 则返回一个绑定了部分参数的新函数对象. 通过柯里化, 我们可以将通用函数定制成满足特定需求的各种函数. 

```{code} javascript
:linenos:
:filename: api_fetching.js
:emphasize-lines: 12-14,17,18

// HTTP request function
function makeRequest(method, baseUrl, endpoint, params) {
  const url = `${baseUrl}${endpoint}`;
  console.log(`${method} ${url}`, params ? `with params: ${JSON.stringify(params)}` : '');
  // example only
  return Promise.resolve({ method, url, params });
}

const curriedRequest = curry(makeRequest);

// 绑定方法(method)和baseUrl
const apiRequest = curriedRequest('GET')('https://api.example1.com');

// 绑定endpoint
const getUserData = apiRequest('/users');
const getPostData = apiRequest('/posts');

// 绑定不同的方法和baseUrl
const postRequest = curriedRequest('POST')('https://api.example2.com');

// 绑定endpoint
const createUser = postRequest('/users');

// 绑定params后, 所有参数均已绑定, 函数被调用
getUserData({ id: 123 });
// Output: GET https://api.example.com/users with params: {"id":123}

getPostData({ userId: 456 });
// Output: GET https://api.example.com/posts with params: {"userId":456}

createUser({ name: 'John', email: 'john@example.com' });
// Output: POST https://api.example.com/users with params: {"name":"John","email":"john@example.com"}

```

## 类型系统

纯函数式模型中的`类型系统`强大且高度一致, `它以极简的形式统一了数据类型定义与枚举声明`. 其他类型系统通常都是它的子集, 因此理解纯函数式模型的类型系统, 几乎等同于理解所有语言中的类型系统. 

### 基础类型

首先, 和其他语言一样, 纯函数式模型也包含一组`基础类型`:

-  基础类型: Int, Float, String, Char  
-  基本组合类型: list, tuple, 写作如 `[Int]`, `(Int, Float)`  
-  函数类型: 例如 `Name :: Int -> Int -> Int -> Int`

:::{hint} `Name :: Int -> Int -> Int -> Int`是什么?
简单而言, 它是意思是`(Int, Int, Int) -> Int`这样的函数. 

实际上这是一个curry函数的定义, 你可以在任意链条上加上括号来看, 譬如:

- `(Int)` -> `(Int -> Int -> Int)`: 参数为Int, 返回值为`(Int -> Int -> Int)`这样的函数, 当你传入一个Int, 就会得到这样的函数
- 或者, `(Int -> Int)` -> `(Int -> Int)`: 参数为(Int, Int), 返回值为`(Int -> Int)`这样的函数, 当你传入两个Int, 就会得到这样的函数
- 或者, `(Int -> Int -> Int)` -> `Int`: 参数为(Int, Int, Int), 返回值为Int, 当你传入三个Int, 就会得到Int返回值
:::

对于`复杂类型`, 可以定义`类型别名`, 例如 `type A = (Int, (Float, String))`.   

这些类型声明常用于类型校验, 拥有准确类型声明的语言, 运行时几乎不会发生类型错误. 

### record类型

接下来是强大的record类型, 类似于其他语言中的struct或dataclass. 

```{code} haskell
data Person = Person {name :: String, age :: Int}
```

在定义类型Person时, 有三个“函数”同时被定义, 分别是`Person`, `name`, `age`.

- `person = Person "Bob" 42`, 调用Person来创建
- `name person`, 在person上调用以获取name字段
- `age person`, 在person上调用以获取age字段.

当我们不需要字段名的时候, 也可以使用tuple风格定义. 对一些不言自明的数据类型, 我们可以采用这种简洁定义.

```{code} haskell
data Response = Response String
```

### enum类型

```{code} haskell
data Status = Alive | Dead
```

这里Alive和Dead就像是symbol一样, Status类型有两种“值”Alive或者Dead.

这里enum也可以是带有数据的. 所以我们可以

```{code} haskell
data Status = Alive {age :: Int, healthy :: Bool} | Dead

-- or
data Status = Alive Int Bool | Dead 
```

### generic data type

这里`age :: Int`是写死的数据, 我们也可以不把这个类型写死, 而是给出一个`generic type`, 类比于其他语言中的类型模版. 


```{code} haskell
:caption: 这里a代表任意类型. 这样一来`Tree 10`和`Tree "bob"`都是合法的.

data Tree a = Nil | Leaf a
```

甚至, 我们可以递归定义类型

```{code} haskell
data Tree a = Nil | Leaf a | Node (Tree a) (Tree a) a

--
data Tree a = Nil | Leaf a | Node {left :: Tree a, right :: Tree a, value :: a}
```

我们甚至可以在其中约束类型"a"的可能性.

```{code} haskell
-- Num a => 意思是a必须是Num类型的, 譬如Int, Float等.
data Tree a = Num a => Nil | Leaf a | Node (Tree a) (Tree a) a
```

### 类型系统

从上面一系列的例子可以看出来, 

- 我们既可以定义数据类型, 类似于struct或dataclass
- 又可以把若干种不同的数据类型组合起来构成一个新类型, 类似于定义enum
- 可以定义generic type, 类似于template
- 还可以限定这个generic type, 类似于[concept](https://en.cppreference.com/w/cpp/language/constraints.html)

等于同时在一个类型系统中集成了struct, enum, template和concept, 四种概念.

:::{hint} Concept是什么
C++中的concept是一种用于指定模板参数约束的机制, 用来在编译时检查类型是否满足特定条件. 
:::

当我们综合起来, 可以得到这样的通用二叉树的定义.

```{code} haskell
data Tree a = Num a => Nil | Leaf a | Node {left :: Tree a, right :: Tree a, value :: a}
```

除此之外, 我们还能够定义"interface", 并在类型上实现.\
在haskell中我们使用class来做到这一点, 这里class并不是OOP中的类关键词, 而是类似于interface, haskell中被称为type class.

```{code} haskell
:linenos:

-- type Class definition
class Eq a where
  (==) :: a -> a -> Bool

-- Instance implementation
instance Eq Tree a where
  Nil == Nil = True
  Leaf x == Leaf y = x == y
  Node l1 r1 v1 == Node l2 r2 v2 = l1 == l2 && r1 == r2 && v1 == v2
  _ == _ = False

equal :: Eq a => Tree a -> Tree a -> Bool
equal x y = x == y  -- 现在可以直接在两个Tree对象上使用==了
```

这样的类型系统被不少现代语言借鉴, 譬如在rust中就有类似的enum机制.

```{code} rust
:linenos:
:filename: generic_binary_tree.rs

enum Tree<T> {
    Nil,
    Leaf(T),
    Node {
        left: Box<Tree<T>>,
        right: Box<Tree<T>>,
        val: T,
    },
}
```

## Monad

### 非函数式角度

首先, 我们尝试用非函数式语言来阐述monad的概念. 

Monad是一类“智能”数据容器. 例如, 调用`Maybe.of(5)`, 就是将整数5放入一个名为Maybe的monad对象中. `用户可以向该对象传递函数, monad在应用这些函数修改内部值的同时, 能够自动处理错误, 异常, 副作用或特定业务逻辑`. 在保证函数式风格的前提下, 大大简化了必要的处理流程. 

一般来说, monad提供三个核心方法作为接口: 

-  **of**: 创建monad对象的方法, 将值封装进monad中. 
-  **map**: 传入用于修改内部数据的函数, 对内部值进行转换. 
-  **flatMap**(或bind): 传入将当前monad转换成另一个monad的函数, 实现链式操作和嵌套扁平化. 

```{code} javascript
:linenos:
:filename: maybe_monad.js
:emphasize-lines: 14-17,19-22
:caption: 用户可以通过map或者flatMap向Maybe对象传递函数, Maybe对象`在应用这些函数的时候能根据自身value是否是null来判断是应用函数还是忽略它们`.

class Maybe {
  constructor(value) {
    this.value = value;
  }

  static of(value) {
    return new Maybe(value);
  }

  static nothing() {
    return new Maybe(null);
  }

  // map用来接收 "直接修改monad中值"的函数
  map(fn) {
    return this.value === null ? Maybe.nothing() : Maybe.of(fn(this.value));
  }

  // flatMap用来接收 "通过monad中的值算出另一个monad"的函数
  flatMap(fn) {
    return this.value === null ? Maybe.nothing() : fn(this.value);
  }

  isNothing() {
    return this.value === null;
  }
}

Maybe.of(42);                 // Maybe { value: 42 }
Maybe.of(5).map(x => x * 2);  // Maybe { value: 10 }
Maybe.of(5).flatMap(x => Maybe.of(x * 2));  // Maybe { value: 10 }

```

monad解决什么问题呢? 我们来看下面这个例子.

```{code} javascript
:linenos:
:filename: get_user_email.js
:emphasize-lines: 11-16
:caption: maybe对象接管了当前值是否为null的判断, 如果值为null后续的传入的函数均被忽略.

// 不使用monad时, 代码冗长混乱
function getUserEmail(userId) {
  const user = getUser(userId);
  if (user === null) return null;
  const profile = getProfile(user.profileId);
  if (profile === null) return null;
  return profile.email;
}

// 使用monad之后, 代码十分清晰, 异常处理由monad负责
function getUserEmailSafe(userId) {
  return Maybe.of(userId)
    .flatMap(id => Maybe.of(getUser(id)))
    .flatMap(user => Maybe.of(getProfile(user?.profileId)))
    .map(profile => profile?.email);
}
```

在上述例子中, `getUser`和`getProfile`可能因各种原因未能获取到相应数据而返回`null`. 通常代码中需要对这种失败情况进行判断. 

但如果引入`Maybe` monad, 当`Maybe`中的值为`null`时, 传递给它的任何函数都不会执行, 且直接返回`null`. 通过这种方式, 我们将`if null`的判断逻辑隐藏在monad内部, 从而保持函数式风格并简化代码. 

下面是另一个类似的monad——`Either`. 它用于处理可能出错的计算, 如除以零, 负数开方等. 

```{code} javascript
:linenos:
:filename: either.js
:emphasize-lines: 15-17,19-21
:caption: 一旦`isLeft`为`True`, 表示计算出错, 后续的计算函数均不执行(被熔断), 直到调用`fold`显式处理错误或计算结果. 

class Either {
  constructor(value, isLeft = false) {
    this.value = value;
    this.isLeft = isLeft;
  }

  static right(value) {
    return new Either(value, false);
  }

  static left(value) {
    return new Either(value, true);
  }

  map(fn) {
    return this.isLeft ? this : Either.right(fn(this.value));
  }

  flatMap(fn) {
    return this.isLeft ? this : fn(this.value);
  }

  fold(leftFn, rightFn) {
    return this.isLeft ? leftFn(this.value) : rightFn(this.value);
  }
}

// Usage example
function divide(a, b) {
  return b === 0 ? Either.left("Division by zero") : Either.right(a / b);
}

function sqrt(x) {
  return x < 0 ? Either.left("Negative square root") : Either.right(Math.sqrt(x));
}

// Chaining operations
const result = Either.right(16)
  .flatMap(x => divide(x, 4))  // Right(4)
  .flatMap(x => sqrt(x))       // Right(2)
  .fold(
    error => `Error: ${error}`,
    value => `Success: ${value}`
  );

console.log(result); // "Success: 2"
```

#### 其他常见的monad(选读)

::::{tab-set}

:::{tab-item} IO
```{code} javascript
:linenos:
:filename: io_monad.js
:caption: IO主要负责组织IO操作, 并推迟执行直到最终调用run

class IO {
  constructor(effect) {
    this.effect = effect;  // 这里effect是一个无参数的函数
  }

  // map传入的函数f能够利用this.effect的返回值, 并返回另一个值
  // 把effect得到的结果传递给函数f, 但是这个过程被封装在另一个函数中, 被延迟执行.
  map(f) {
    return new IO(() => f(this.effect()));
  }

  // flatMap传入的函数f能够利用this.effect的返回值, 并返回另一个IO monad
  // 这里的f通常也是一种IO操作
  // 这里把所有计算串起来, 但是延迟执行
  flatMap(f) {
    return new IO(() => f(this.effect()).effect());
  }

  // run the side effect
  run() {
    return this.effect();
  }
}

// Usage example:
const readLine = new IO(() => prompt("Enter your name:"));
const printLine = (msg) => new IO(() => console.log(msg));

const program = readLine.flatMap(name =>
  printLine("Hello " + name)
);

program.run();

```
:::

:::{tab-item} List
```{code} javascript
:linenos:
:filename: list_monad.js
:caption: List这个monad比较好理解, 唯一让人惊奇的是, List居然也可以是个monad!

class List {
  constructor(values) {
    this.values = values;
  }

  map(f) {
    return new List(this.values.map(f));
  }

  flatMap(f) {
    return new List(this.values.flatMap(x => f(x).values));
  }
}

// Usage example:
const nums = new List([1, 2, 3]);
const result = nums.flatMap(x => new List([x, x * 10]));
console.log(result.values); // [1, 10, 2, 20, 3, 30]
```
:::

:::{tab-item} State
```{code} javascript
:linenos:
:filename: state_monad.js
:caption: State负责状态转移以及根据当前状态算出value

class State {
  constructor(runState) {
    this.runState = runState; // function: state => [value, newState]
  }

  // 这里函数f只修改runState产生的value, 并不会影响runState本身.
  map(f) {
    return new State(state => {
      const [value, newState] = this.runState(state);
      return [f(value), newState];
    });
  }


  // 这里的函数f由value初始化, 返回一个State monad, 这个monad负责状态转移.
  flatMap(f) {
    return new State(state => {
      const [value, newState] = this.runState(state);
      return f(value).runState(newState);
    });
  }
}

// Usage example:
const getState = new State(state => [state, state]);
const putState = newState => new State(() => [null, newState]);

const increment = getState.flatMap(n =>
  putState(n + 1).map(() => n)
);

// Run with initial state 0:
const [oldValue, finalState] = increment.runState(0);
console.log(oldValue);   // 0
console.log(finalState); // 1
```
:::
::::

### 从函数式角度

从函数式角度来看, 与monad相关的概念主要有三个:functor, applicative和monad, 它们都是接口, 提供一定方法, 旨在简化代码并提供额外功能. 

-  **Functor** 提供了`fmap`方法(对应上文的`map`), 用于修改monad内部的值. 
-  **Applicative** 提供了`<*>`操作符, 支持串联计算, 例如 `monad(fn(x, y)) <*> monad(value1) <*> monad(value2)`. 
-  **Monad** 提供了`>>=`操作符(对应上文的`flatMap`), 支持从一个monad映射到另一个monad. 

| **特性**     | **Functor**            | **Applicative**        | **Monad**                      |
| ------------ | ---------------------- | ---------------------- | ------------------------------ |
| **操作符**   | `fmap` 或 `<$>`        | `<*>` 和 `pure`        | `>>=` 和 `return`              |
| **核心能力** | 对上下文中的值应用函数 | 应用上下文中的函数到值 | 顺序执行相互之间有依赖的计算   |
| **依赖关系** | 无                     | 无(支持并行)           | 有(后续依赖前置结果)           |
| **典型场景** | 简单变换               | 独立验证, 并行计算     | 顺序IO, 状态管理, 错误传播等等 |

我们从List这个monad开始说明. 

```{code} haskell
:linenos:
:filename: monad_explain.hs

-- 首先List是个Functor, 因此它支持fmap函数应用另一个函数在List上
fmap (*2) [1, 2, 3] -- (*2)是一个函数, 把入参*2后返回, 最终原List中的值被修改得到[2, 4, 6]这样一个List


-- 其次List是个Applicative, 存到List中的函数, 也可以应用到其他List上
[(+1), (*2), (-3)] <*> [1, 2]  -- 得到[2, 2, -2, 3, 4, -1]
pure 3 :: [Int]  -- 得到[3]

-- 最后List是个Monad, 它允许你把一个函数应用到容器里的值上, 而这个函数本身返回一个容器, 不过最终结果会被"扁平化"
[1, 2, 3] >>= \x -> [x, x * 10]  -- 这里>>=等于flatMap, 把λ x -> [x, x*10]这个函数应用在[1,2,3]上, 最后得到[1, 10, 2, 20, 3, 30]
```

这里只是简化介绍, 感兴趣的话可以参考[^haskell-book].

不过究其本质和实用性, haskell中的例子跟上面javascript的例子没有太多区别, 只不过代码风格略有区别.

因为函数式编程中对monad的介绍相对晦涩难懂, 且常被人误解或[调侃](https://monad-tutorial.vercel.app). 

## 什么时候才用Functional Model?

从实用主义角度来看, 我**不建议在日常工作中采用纯函数式语言**. 理由如下: 

1. 会写纯函数式语言的人较少
2. 能写好的人更少
3. 能写得又好又快的人更是凤毛麟角
4. 目前没有主流系统采用纯函数式模型编写

从理性主义角度来看, 至少**不应使用纯函数式语言来编写系统原型**. 因为系统原型需要快速构建, 且经常不断修改, 最终收敛于正确的业务逻辑. \
此外, 从性能角度考虑, **如果系统对性能要求高且需持续优化, 这类系统也不适合采用纯函数式语言**. 

根据个人经验, 以下几个场景适合使用纯函数式模型: 

-  `用函数式模型重构部分命令式代码`, 例如通过组合各种高阶函数实现业务逻辑, 通过引入合适的monad处理异常, 副作用或保护业务数据. 局部重构能稳固逻辑, 提升代码可读性, 且相对简单. 这是我日常最常用纯函数式模型的场景. 
-  实现业务无关的算法时, 使用纯函数式模型同样合适, 因为这类算法相对稳定, 不易频繁变更. 

但在`重构时, 应优先保持整体代码的一致性`. 例如, 若代码库已有成熟的异常处理风格, 则无必要单独引入monad. 不能为了使用函数式而刻意使用. 

综上, `局部采用纯函数式模型能显著提升代码可读性并减少bug`, 但整体系统采纳纯函数式模型, 至少目前来看并不推荐, 尤其当业务多变时更应谨慎. 

---

[^haskell-book]: [programming in Haskell](https://book.douban.com/subject/26851474/), 作者Graham Hutton, 2016年出版