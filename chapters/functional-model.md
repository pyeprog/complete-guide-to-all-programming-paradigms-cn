# Pure Functional

![[Think 2025-06-24 10.36.28.excalidraw]]
之前我们提到了声明式 模型(declarative model), 这个模型中没有可变的状态, 很多人其实已经把声明式模型称为functional model(函数式模型), 但在声明式模型中, 也存在负责和外界IO的函数, 并且也会添加try catch等机制来处理异常. 所以它并不是纯粹的函数式模型.

与之对应, 这里要介绍的pure functional model在declarative model的基础上把函数式和不可变性走到极致. 纯函数这个概念类似于数学中定义的函数, 给定一个输入, 总是得到一个输出, 没有副作用(不会修改全局变量, 没有IO操作, 不会改变状态等等). 为了让纯函数式编程变得有用, 我们必须引入IO操作. 纯函数式模型使用monad把IO, 异常等等不可避免的副作用通通隔离起来, 做到纯粹的函数式. 这个后面会提到.

虽然日常工作中, 我们基本不会使用纯函数式语言(譬如haskell)写项目, 但其模型中的种种机制, 其实早就被融合到当下几乎所有的主流语言中. 几乎所有现代语言都会把函数作为第一类公民. 几乎每种非函数式语言都会存在函数式的库或者包, 更别说一些高阶函数甚至直接被集成在标准库中. 纯函数式语言的类型系统被借鉴, 成为其他语言中的parametrized enum. 而monad被用来解决null判断和处理副作用等等. 所以, 纯函数式模型还是值得了解一番.

## Expression First的代码风格

相比于其他语言, 纯函数式语言首先在风格上就有显著不同.  我们来看两个例子.
大多数语言中代码是由语句(statement)构建的, 编程即堆叠计算或命令的语句, 而pure functional language中几乎所有的元素都是表达式(expression), 编程则是嵌套组织表达式. 而且在绝大多数情况下, pure functional language中函数的函数体有且只有一个嵌套的表达式, 这是因为pure functional language中绝大多数都表达式是没有副作用的, 如果把没有副作用的表达式堆叠起来顺序执行, 函数也仅能返回其中一个表达式的结果, 其他的表达式即使执行了, 因为没有副作用, 也跟没执行没有区别. 可以说, 只要强调无副作用, 那么该语言基本都会偏向expression first的代码风格.
![[Think 2025-06-19 17.39.06.excalidraw]]

其他语言也逐步在采纳这种代码风格, 我们常见的if/else, loop, pattern matching(including assigning)也都可以被改成表达式, 只要让它们都可以最终计算得到一个值即可. 这种风格可以大大提升代码的表现力.

```rust
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
  if idx >= numbers.len() { break acc; }
  acc += numbers[idx];
  idx += 1;
    }
}

```

## 高阶函数和curry函数

就像object model说一切皆对象, pure functional model说一切都是数据和函数.
首先介绍一些常用的高阶函数, 这几乎是所有函数式模型的标配. 也是我们使用最频繁, 最能提升代码可读性的函数式元素.

```explaintext
// map (in python)
list(map(lambda x: x**2, [1, 2, 3])) == [1, 4, 9]

// filter (in python)
list(filter lambda x: x % 2 == 0, [1, 2, 3, 4]) == [2, 4]

// reduce or fold (in python)
(0 + 1 + 2 + 3) == reduce(lambda acc, x: acc + x, [1, 2, 3], 0)

// foldl (in haskell), foldl means fold from left
total = foldl (+) 0 [1, 2, 3]

// sort (in python)
sorted([2, 3, 1, 4]) == [1, 2, 3, 4]

// forEach (in javascript), which executes side effect on each item
[1, 2, 3].forEach(console.log)

// flatmap (in scala), which is map then flat
val lists = List(List(1, 2), List(3, 4))
val flat = lists.flatMap(x => x)  // List(1, 2, 3, 4)

// zipWith (in haskell)
pairs = zipWith (+) [1, 2, 3] [4, 5, 6]  -- which returns [5, 7, 9]

// compose (in python, from package called toolz)
add5 = lambda x: x + 5
mul10 = lambda x: x * 10
div3 = lambda x: x / 3
calculate = compose(add5, mul10, div3)
calculate(3) == 5 + (10 * (3 / 3))
calculate(3) == add5(mul10(div3(3)))

// takeWhile, dropWhile (in haskell)
takeWhile (<3) [1, 2, 3, 4] -- which returns [1, 2]
dropWhile (<3) [1, 2, 3, 4] -- which returns [3, 4]

// groupBy (in python)
words = ["cat", "apple", "cherry", "dog"]
groupby(words, key=len)  # which groups [cat, dog], [apple], [cherry]

// memoize (in python, from package called toolz)
def factorial(x):
 if x <= 1:
  return 1
 return x * factorial(x - 1)

factorial_with_memo = memoize(factorial)
factorial_with_memo(1000)  # slow
factorial_with_memo(1000)  # super fast

```

此外, 函数的curry化, 或者说curry函数, 是另一个非常好用, 也非常常用的特性. 和高阶函数配合起来能大大简化代码. curry化之后, 函数只有在给足全部参数后才会被调用, 如果只给一部份参数, 则会返回绑定了部份参数的另一个函数对象. 通过curry化, 我们可以把通用的函数订制成满足需求的各种函数.

```javascript
// HTTP request function
function makeRequest(method, baseUrl, endpoint, params) {
  const url = `${baseUrl}${endpoint}`;
  console.log(`${method} ${url}`, params ? `with params: ${JSON.stringify(params)}` : '');
  // example only
  return Promise.resolve({ method, url, params });
}

const curriedRequest = curry(makeRequest);

// Create API-specific request builders
const apiRequest = curriedRequest('GET')('https://api.example.com');
const getUserData = apiRequest('/users');
const getPostData = apiRequest('/posts');

// Different HTTP methods
const postRequest = curriedRequest('POST')('https://api.example.com');
const createUser = postRequest('/users');

// Usage
getUserData({ id: 123 });
// Output: GET https://api.example.com/users with params: {"id":123}

getPostData({ userId: 456 });
// Output: GET https://api.example.com/posts with params: {"userId":456}

createUser({ name: 'John', email: 'john@example.com' });
// Output: POST https://api.example.com/users with params: {"name":"John","email":"john@example.com"}
```

## 类型系统

纯函数式模型中的类型系统, 是强力且非常一致的类型系统. 它以非常简洁的形式统一了数据类型定义和enum声明. 其他类型系统都是他的子集, 理解纯函数式模型中的类型系统约等于理解了所有语言中的类型系统.

首先和其他所有语言一样, 纯函数式模型也有一组基础类型.

- 基础类型: Int, Float, String, Char
- 基本组合类型: list, tuple, 写作`[Int]`, `(Int, Float)`
- 函数类型: Name :: Int -> Int -> Int -> Int
对于复杂的类型, 我们可以定义类型别名, 譬如`type A = (Int, (Float, String))`
这些类型声明经常被用作类型校验, 有准确的类型声明的语言, 类型错误在runtime的时候基本不会发生.

接下来是强大的自定义数据类型
首先是record类型, 类似于其他语言中的struct或者dataclass

```haskell
data Person = Person {name :: String, age :: Int}
```

在定义类型Person时, 有三个“函数”同时被定义, 分别是Person, name, age.

- `person = Person "Bob" 42`, 调用Person来创建
- `name person`, 调用name来获取name字段
- `age person`, 调用age来获取age字段.

当我们不需要字段名的时候, 也可以定义tuple风格的record. 对一些不言自明的数据类型, 我们可以采用这种简洁定义.

```haskell
data Response = Response String
```

接着是类似于enum的定义.

```haskell
data Status = Alive | Dead
```

这里Alive和Dead就像是symbol一样, Status类型有两种“值”Alive或者Dead.

这里enum也可以是带有数据的. 所以我们可以

```haskell
data Status = Alive {age :: Int, healthy :: Bool} | Dead
data Status = Alive Int Bool | Dead  -- or we can
```

这里`age :: Int`是写死的数据, 但我们也可以给定义generic type, 类比于其他语言中的类型模版. 这里a代表任意类型. 这样一来`Tree 10`和`Tree "bob"`都是合法的.

```haskell
data Tree a = Nil | Leaf a
```

甚至, 我们可以递归定义类型

```haskell
data Tree a = Nil | Leaf a | Node (Tree a) (Tree a) a
data Tree a = Nil | Leaf a | 
 Node {left :: Tree a, right :: Tree a, value :: a}
```

我们甚至可以在其中约束“a“可能的类型.

```haskell
-- Num a denotes that a must be a number type
data Tree a = Num a => Nil | Leaf a | Node (Tree a) (Tree a) a
```

从上面一系列的例子可以看出来, 我们既可以定义数据类型, 又可以把若干种不同的数据类型组合起来构成一个新类型. 可以定义generic type, 还可以限定这个generic type. 等于同时在一个类型系统中集成了struct, enum, template和concept, 四种概念.

```haskell
data Tree a = Num a => Nil | Leaf a | 
 Node {left :: Tree a, right :: Tree a, value :: a}
```

除此之外, 我们还能够定义接口, 并在类型上实现接口. 这里class并不是OOP中的class. 而是类似于interface, 被称为type class.

```haskell
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
equal x y = x == y  -- it's possible to use == now
```

这样的类型系统被不少现代语言借鉴, 譬如在rust中就有类似的enum机制.
![[Think 2025-06-19 21.47.33.excalidraw]]

## Monad

### 非函数式角度

首先我们尝试用非函数式的语言来阐述一下monad.
monad是一类“智能”数据容器. 譬如Maybe.of(5), 我们就把5这个整数放入了一个名为Maybe的monad对象中. 用户能够传函数给这个对象, 对象在用函数修改其中的值的时候, 也能够自动的处理错误, 异常, 副作用或者特定的业务逻辑. 在保证函数式风格的前提下, 大大简化必要的处理.

它一般提供3个方法作为接口.

- 创建monad对象的方法of.
- 传入修改内部数据的方法map.
- 传入把当前monad转换成其他monad的方法flatMap.

```javascript
// With Maybe monad
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

  map(fn) {
    return this.value === null ? Maybe.nothing() : Maybe.of(fn(this.value));
  }

  flatMap(fn) {
    return this.value === null ? Maybe.nothing() : fn(this.value);
  }

  isNothing() {
    return this.value === null;
  }
}

Maybe.of(42)  // Maybe { value: 42 }
Maybe.of(5).map(x => x * 2)  // Maybe { value: 10 }
Maybe.of(5).flatMap(x => Maybe.of(x * 2))  // Maybe { value: 10 }
```

那它处理什么问题呢?

```javascript
// Traditional null handling without monad(messy)
function getUserEmail(userId) {
  const user = getUser(userId);
  if (user === null) return null;
  const profile = getProfile(user.profileId);
  if (profile === null) return null;
  return profile.email;
}

function getUserEmailSafe(userId) {
  return Maybe.of(userId)
    .flatMap(id => Maybe.of(getUser(id)))
    .flatMap(user => Maybe.of(getProfile(user?.profileId)))
    .map(profile => profile?.email);
}
```

上面的例子中getUser和getProfile可能因为各种原因无法找到相应的数据而返回null. 一般代码中我们需要就这个失败情况进行判断. 但是如果引入maybe monad, 如果maybe中的值是null, 那么任何传递给他的函数都不再执行, 并直接返回null. 通过这种方式, 我们把if null的判断藏在了monad定义中. 由此保持了函数式风格, 并简化了代码.

一下是另一个类似的monad, Either. 它用来处理一些会报错的计算, 譬如除0, 负数开方等等. 一旦isLeft是True, 此时计算已经出错, 任何后续的计算函数都不执行. 直到调用fold显式的处理错误或结果.

```javascript
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
  .flatMap(x => divide(x, 4))  // Right(4)
  .flatMap(x => sqrt(x))       // Right(2)
  .fold(
    error => `Error: ${error}`,
    value => `Success: ${value}`
  );

console.log(result); // "Success: 2"
```

### 从函数式角度

从函数式角度而言. 和monad的相关的, 包括monad在内, 有3个概念. 分别是functor, applicative以及monad, 它们都是为了简化代码并提供额外的功能.

- functor提供了fmap方法, 对应上面的map方法. 提供了修改monad内部值的能力
- applicative提供了`<*>`操作符, 提供了串联计算的能力. 譬如`monad(fn(x, y)) <*> monad(value1) <*> monad(value2)`
- monad提供了`>>=`操作符, 对应上面的flatMap方法. 提供了从一个monad映射到另一个monad的能力.

| **特性**   | **Functor**    | **Applicative** | **Monad**        |
| -------- | -------------- | --------------- | ---------------- |
| **操作符**  | `fmap` 或 `<$>` | `<*>` 和 `pure`  | `>>=` 和 `return` |
| **核心能力** | 对上下文中的值应用函数    | 应用上下文中的函数到值     | 顺序执行依赖的计算        |
| **依赖关系** | 无              | 无（并行）           | 有（后续依赖前置结果）      |
| **典型场景** | 简单变换           | 独立验证、并行计算       | 顺序 IO、状态管理、错误传播  |

```haskell
-- data Maybe a = Just a | Nothing
add3 :: Int -> Int
add3 x = x + 3
add3 <$> Just 2  -- 等价于：fmap add3 (Just 2)，结果：Just 5
add3 <$> Nothing -- 结果：Nothing（上下文不变，函数未执行）
add3 <$> [1, 2, 3]  -- 等价于：map add3 [1, 2, 3]，结果：[4, 5, 6]

Just (+3) <*> Just 2
[(+1), (*2)] <*> [3, 4]  -- 结果：[4, 5, 6, 8], List是applicative
```

```haskell
-- Maybe Monad示例
import Control.Monad (liftM, ap)

-- Maybe类型的定义
data Maybe a = Nothing | Just a

-- 实现Functor实例
instance Functor Maybe where
    fmap _ Nothing = Nothing
    fmap f (Just x) = Just (f x)

-- 实现Applicative实例
instance Applicative Maybe where
    pure = Just  -- `pure a` means `Just a`
    Nothing <*> _ = Nothing
    (Just f) <*> mx = fmap f mx

-- 实现Monad实例
instance Monad Maybe where
    return = pure   -- `return a` means `Just a`
    Nothing >>= _ = Nothing
    (Just x) >>= f = f x

-- 常见用途示例：处理可能失败的计算
safeDiv :: Int -> Int -> Maybe Int
safeDiv _ 0 = Nothing
safeDiv x y = Just (x `div` y)

safeSqrt :: Int -> Maybe Int
safeSqrt x
    | x < 0 = Nothing
    | otherwise = Just (floor (sqrt (fromIntegral x)))

-- 使用do表示法的顺序计算
calculate :: Int -> Int -> Maybe Int
calculate a b = do
    quotient <- safeDiv a b
    result <- safeSqrt quotient
    return (result + 1)

-- 使用Monad的>>=操作符的计算
calculate' :: Int -> Int -> Maybe Int
calculate' a b = 
    safeDiv a b >>= \quotient ->
    safeSqrt quotient >>= \result ->
    return (result + 1)
```

这里因为时间关系就不再深入了. 感兴趣的话可以参考《programming in Haskell》.
究其本质和实用性, haskell中的实践跟上面javascript的例子没有太多区别.
其实纯函数式的概念并不复杂, 但复杂的概念和术语妨碍我们拥抱它. 这在实用主义者的角度来看, 是一场悲剧, 因为它的确更看重形式的严谨而不是实用性.

## 什么时候才用pure Functional Model?

以实用主义的角度来看, 我不建议在日常工作中采用pure functional language. 理由1, 会写的人少; 理由2, 能写好的人更少; 理由3, 能写的又好又快的人更是凤毛麟角; 理由4, 目前没有主流系统用这个模型编写. 而以理性主义角度来看, 至少不要用pure functional language来编写系统原形. 因为系统原形需要快速构建, 并且系统原形总是要不断的修改, 最终收敛于正确的业务逻辑. 另外从性能角度来讲, 如果系统要求高性能, 并且要求性能能够持续改进, 这样的系统也不适合pure functional language.

以个人经验而言, 以下几个场景是适合使用pure functional model的.
首先, 我们可以用pure functional model去重构部份命令式的代码, 譬如通过组合各种高阶函数实现代码逻辑, 通过引入合适的monad去处理异常, 副作用或保护业务数据. 这种局部的重构能够稳固逻辑, 提升代码可读性, 而且重构一小块代码, 也相对简单. 这是我日常最常用pure functional model的地方. 此外, 在实现业务无关的算法的时候, 使用pure functional model也是合适的. 因为这种算法一般相对稳固, 不会轻易去改变算法逻辑.
不过在进行重构时, 应该优先保持整体代码的一致性. 譬如代码库中已经使用了一种风格的异常处理, 这个时候再引入monad就没有必要. 我们不能为了使用函数式而使用.

综上, 如果局部使用pure functional model, 能够极大的提升代码可读性并减少bug. 但是整体系统采纳pure functional model, 至少就目前现状来看, 并不推荐, 如果业务多变, 就更是如此.
