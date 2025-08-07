# Object Oriented Programming Model

虽然关于“为什么OOP很糟糕”的讨论层出不穷，但OOP依然是事实上的最流行编程范式。OOP是一种表现力极强的模型，而强大的模型往往伴随着各种误用和滥用，因此如何正确运用OOP成为一门值得钻研的学问。具体的OOP语法，任何一本OOP语言的书籍都会详尽介绍，这里不再赘述。本文重点讨论OOP中的重要特性及其最佳实践。

:::{image} ../material/huge-amount-of-oop.png
:::

## 为什么OOP流行

OOP之所以流行，主要原因包括：

-  `OOP符合人类的直觉`，[本体隐喻](https://www.bilibili.com/video/BV13o4y1Q7Gq/)是人类赖以生存的[隐喻系统](https://book.douban.com/subject/26298597/)的一部分，而OOP提供了本体隐喻的具体实践。
-  相较于基于对象的模型，OOP引入了class，即对象的蓝图，使我们能够`通过声明式方式定义对象`。在静态语言中，这有助于编译器提升性能。更重要的是，class带来了更强的约束，使对象创建后不能随意扩展（至少不易扩展）和修改。
-  `OOP具备强大的模仿能力`:
   - 类本身可以作为type，我们可以在语言中自定义type，并提供与type相关的操作符或函数。
   - 类可以被视为一种module，实际上类与module的界限非常模糊，除实例化外，类的行为与module几乎一致。提供封装、访问控制和接口方面不相上下，甚至表现得更好。
   - 如果重载了`()`操作符，实现了某种内置函数（如`__call__`），或实现了某些trait或interface，使对象能够像函数一样“被调用”。类中的数据被保护，不可被外界直接访问，类似于函数的闭包。

由于OOP提供了这种极具通用性的模仿能力，它可以用来改造语言、构造{abbr}`领域专用语言(Domain Specific Language)`，使其更贴近业务逻辑。这正是{abbr}`领域驱动设计(Domain Driven Design, DDD)`的核心要义。

```{code} python
:linenos:
:filename: oop_capability.py

# as type
class Point:
    def __init__(self, x, y): 
     self.x, self.y = x, y
     
    def __add__(self, other): 
     return Point(self.x + other.x, self.y + other.y)
     
    def __str__(self): 
     return f"({self.x}, {self.y})"

p1 = Point(1, 2)
p2 = Point(3, 4)
result = p1 + p2  # Point(4, 6)

# as module
class MathUtils:
    PI = 3.14159
    _private_constant = 42

    @staticmethod
    def square(x): return x * x

    @classmethod
    def circle_area(cls, radius): return cls.PI * radius * radius

# as callable
class Multiplier:
    def __init__(self, factor):
        self.__factor = factor  # private data

    def __call__(self, value):
        return value * self.__factor

double = Multiplier(2)
result = double(5)  # 10
```

## OOP的不同风格

OOP有多种不同的风格, 以下介绍三种.

::::{tab-set}

:::{tab-item} class风格
```{code} java
:linenos:
:filename: classStyle.java
:caption: 这也是最常见的风格, 我们通过class关键词创造一个class, 可以指定父类来继承, 可以指定interface对象来实现, 一般都会存在构造函数, 以及析构函数. 数据和方法都应在class内.

// 接口定义
interface InterfaceExample {
    void interfaceMethod();
}

// f父类
class ParentClass {
    public ParentClass() {
        System.out.println("ParentClass constructor");
    }

    public void parentMethod() {
        System.out.println("Parent method");
    }

    protected void finalize() throws Throwable {
        System.out.println("ParentClass destructor");
        super.finalize();
    }
}

// 子类继承父类, 并实现接口
public class ChildClass extends ParentClass implements InterfaceExample {
    public ChildClass() {
        super(); 
        System.out.println("ChildClass constructor");
    }

    @Override
    public void interfaceMethod() {
        System.out.println("Implemented interface method");
    }

    @Override
    protected void finalize() throws Throwable {
        System.out.println("ChildClass destructor");
        super.finalize();
    }

    public static void main(String[] args) {
        ChildClass obj = new ChildClass();
        obj.parentMethod();
        obj.interfaceMethod();
    }
}
```
:::

:::{tab-item} struct+impl风格
```{code} rust
:linenos:
:filename: struct_impl_style.rs
:caption: 在这种风格中, struct首先被定义, 随后通过impl关键词在其上定义方法. 这样的好处是数据定义和方法定义分离, 方法可以补充定义

// 定义一个长方形结构体, 其中只有数据
struct Rectangle {
    width: u32,
    height: u32,
}

// 在长方形上实现一些方法
impl Rectangle {
    fn new(width: u32, height: u32) -> Self {
        Self { width, height }
    }

    fn area(&self) -> u32 {
        self.width * self.height
    }

    // 判断是否包含另一个另一个长方体
    fn can_hold(&self, other: &Rectangle) -> bool {
        self.width > other.width && self.height > other.height
    }
}

fn main() {
    let rect1 = Rectangle::new(30, 50);
    let rect2 = Rectangle::new(10, 40);

    println!("The area of rect1 is {}", rect1.area());
    println!("Can rect1 hold rect2? {}", rect1.can_hold(&rect2));
}
```
:::

:::{tab-item} struct+function风格
```{code} c
:linenos:
:filename: struct_func_style.c
:caption: 在没有OOP支持的语言中可以如此实现, 先定义结构体, 然后定义一些操作它们的方法. 本实现使用一些c独有的指针技巧

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// 定义一个专门用来承载函数指针的结构体
typedef struct Shape {
    double (*area)(struct Shape *self);
} Shape;

// Rectangle "class"
typedef struct {
    Shape base;  // base必须是第一个字段
    double width;
    double height;
} Rectangle;

// Circle "class"
typedef struct {
    Shape base;  
    double radius;
} Circle;

// Rectangle area method
double rectangle_area(Shape *shape) {
    // 调用时需要确保shape指向的是Rectangle结构体
    Rectangle *rect = (Rectangle *)shape;
    return rect->width * rect->height;
}

// Circle area method
double circle_area(Shape *shape) {
    Circle *circle = (Circle *)shape;
    return M_PI * circle->radius * circle->radius;
}

// Rectangle"构造函数"
Rectangle *rectangle_new(double width, double height) {
    Rectangle *rect = malloc(sizeof(Rectangle));
    rect->width = width;
    rect->height = height;
    rect->base.area = rectangle_area;  // 组装area方法
    return rect;
}

// Circle的"构造函数"
Circle *circle_new(double radius) {
    Circle *circle = malloc(sizeof(Circle));
    circle->radius = radius;
    circle->base.area = circle_area;  // 组装area方法
    return circle;
}

int main() {
    Shape* shapes[2];

    // 这里的技巧是转换指针类型, 虽然Rectangle的第一个字段是Shape类型的base
    // 但从内存的视角来看, 它的前8byte就是area的函数指针. 
    // 所以Rectangle*转成Shape*, 也能够正常调用
    shapes[0] = (Shape *)rectangle_new(10, 20);
    shapes[1] = (Shape *)circle_new(5);

    for (int i = 0; i < 2; i++) {
        printf("Shape %d area: %.2f\n", i + 1, shapes[i]->area(shapes[i]));
        free(shapes[i]);
    }

    return 0;
}

```
:::

::::

## OOP的不同性质

OOP在不同的语言中有不同的性质. 我们就以下4种性质进行介绍.

### open class / close class

::::{tab-set}

:::{tab-item} open class
```{code} ruby
:linenos:
:filename: app.rb
:emphasize-lines: 7-12
:caption: open class意味着一个类可以补充定义, rust, swift, golang, rust, ruby, scala支持

class App
    def hello()
        "hello"
    end
end

# 补充定义App
class App
    def world()
        "world"
    end
end

app = App.new
puts app.hello() # hello
puts app.world() # world
```
:::

:::{tab-item} close class
```{code} python
:linenos:
:filename: app.py
:caption: close class意味着重复定义类, 要么报错, 要么抹掉之前的定义

class App:
    def hello(self):
        return "hello"

class App:
    def world(self):
        return "world"

app = App()
app.hello() 
#AttributeError: 'App' object has no attribute 'hello'
```
:::

::::

### method bounded / method unbounded

::::{tab-set}

:::{tab-item} method bounded
```{code} cpp
:linenos:
:filename: int_stack.cpp
:caption: method bounded意味着方法跟随类被定义, 它们定义在类的"内部"

class IntStack {
    // ...

    public: 
    void push(int data);
}

IntStack s;
s.push(1);  // 只能通过IntStack的实例调用push方法
```
:::

:::{tab-item} method unbounded
```{code} c
:linenos:
:filename: int_stack.c
:caption: method unbounded意味着方法游离于类定义, 他们定义在类的外部, 我们可以不通过类或对象获取他们

typedef struct {
    ...
} IntStack;

void push(IntStack stack, int data);
```
:::

::::

### 是否支持继承

::::{tab-set}

:::{tab-item} 支持继承
```{code} cpp
:linenos: 
:filename: inheritance.cpp
:caption: 类支持继承

class Worker : public Human {
    ...
}
```
:::

:::{tab-item} 不支持继承
```{code} go
:linenos:
:filename: non_inheritance.go
:caption: 不支持继承, 但会提供额外机制来代替继承
:emphasize-lines: 6

type Human struct {
    ...
}

type Worker struct {
    Human  // Human代理了Worker中的一些数据访问
    ...
}
```
:::

::::

### 接口是否强迫实现方法

::::{tab-set}

:::{tab-item} 强迫实现方法
```{code} rust
:linenos:
:filename: interface_coerced.rs
:emphasize-lines: 3
:caption: fmt::Display强迫Worker实现fmt方法, 换句话说Worker被fmt::Display约束

struct Worker {...}

// fmt::Display是一个trait, 强迫Worker实现fmt方法
impl fmt::Display for Worker {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        ...
    }
}
```
:::

:::{tab-item} 不强迫实现方法
```{code} go
:linenos:
:filename: non_interface_coercion.go
:caption: geometry这个interface并不强迫circle实现area和perim方法(当然, 要正确使用还是必须实现这两个方法的)

type geometry interface {
    area() float64
    perim() float64
}

type circle struct {
    radius float64
}

func (c circle) area() float64 {
    return math.Pi * c.radius * c.radius
}
func (c circle) perim() float64 {
    return 2 * math.Pi * c.radius
}

// interface不会强迫circle去实现area和perim方法, 全凭自觉
```
:::

::::

任何一门OOP语言, `一般都在这些风格和性质中组合出自己的OOP风格`.

## 继承

在介绍OOP的实践之前, 我们需要先展开说明继承这个特性. 这里提到的继承特指**具体类之间的继承(inheritance)**, _不是_继承接口或虚基类(subtyping).

继承是目前OOP被诟病较多的特性, 很多语言公开抛弃继承特性. 大家谈到继承的时候一般会诟病的点是

- 多继承引入了不必要的复杂性
- 继承即耦合, 子类和基类耦合在一起, 基类的改动可能导致子类行为改变甚至错误.

这些诟病的点, 都是确有其事.

一些语言摒弃了多继承抛弃, 另一些引入了额外的特性去解决问题(虚继承). 但`耦合仍旧是继承机制避不开的问题`.

### 继承为什么被诟病

但仍有大量语言坚持支持继承这一特性，原因何在？继承为何被诟病为“糟糕”，但又被广泛保留？问题的根源究竟在哪里？

首先，继承诞生的前提非常合理。\
`引入类和对象后，人们发现大量代码重复`，不同类需要实现相同的方法。要么复制粘贴，导致代码冗余；要么将方法抽离到类外，回归struct+function风格，破坏封装。`为减少代码重复且保护封装，继承被发明出来`。

继承的原始动机也十分合理。`有了继承，可以先抽象再具体编码`，例如Object > Creature > Animal > Mammal > Human，层层递进，逻辑清晰。其次，`当系统需要扩展时，无需重新实现新类，只需继承已有类并实现子类，符合开闭原则的实践`。

:::{caution} 继承的前提与动机无可挑剔，但问题出在假设上。
`先抽象再具体的编码假设架构师能够准确理解业务问题，深谙业务未来走向，能做出正确抽象`。\
只有如此，基类才能提供真正有用的方法和属性，完美契合业务需求，且未来无需修改，耦合原有实现才不会出问题。
:::

然而，这一假设站不住脚。

大量文章、书籍和论文指出，再优秀的业务分析也无法完全洞悉客户需求，`客户需求会随着系统交付不断变化`。再优秀的架构师也难以设计出永远合适的抽象模型，`因为需求持续演变，迟早原有抽象会失效`

:::{figure} ../material/Laws-of-Software-Evolution-Revisited.png
《Laws of Software Evolution Revisited》[^software-evolution]一文指出，系统必须不断修改以适应用户不断变化的需求，停止适应则系统劣化明显，甚至被弃用。即便当下需求被完美适配，系统终将在未来某个时刻变得不再满足需求。
:::

当需要修改时才发现过去与现在通过继承紧密耦合，基类无法随意更改，继续继承又难以推进，系统便走到了生命周期的尽头，最终可能只能重写。

### 什么时候使用继承

所以，我们是否应当完全抛弃继承呢？答案是未必。

如果两个类之间存在明确的Is-A关系，使用继承是合适的。比如，cat is a critter，那么cat类继承自critter类就是合理的。

具体来说，先抽象再具体的编码方式在某些场景下适合使用继承。例如，业务无关且稳定的概念非常适合继承，几何领域中的`shape > rectangle > square`就是一个典型案例。

人们希望通过继承扩展系统本身没有问题，关键在于继承的对象。如果继承的是具体类，容易导致耦合和维护难题；但`如果继承的是稳定的interface或trait`，那么所有实现仅与稳定的API耦合，同时满足开闭原则和依赖反转原则。这种情况下，通常不称为继承（inheritance），而称为创建子类型（subtyping）。

综上, 如果使用继承, 则我们应该谨慎的, 小范围的使用继承, `只有继承能够极大简化实现的时候使用`. `跨模块的继承是绝对要避免的`, 不必要时完全可以用组合, 代理, 甚至函数式编程代替.

### 代替继承

#### 委托

委托(代理)是代替继承的另一种机制. 类似于object based model中对象可以把数据或函数的请求委托给自己的原形. 在OOP中也存在类似的机制.

```{code} go
:linenos:
:filename: delegation.go
:emphasize-lines: 7
:caption: 这里Cat把Legs和Kingdom委托给Animal. 我们可以直接在Cat的实例中访问这两个属性.

type Animal struct {  
        Kingdom string  
        Legs    uint8
}

type Cat struct {  
        Animal // 对cat.Kingdom和cat.Legs代理给Animal
        Sound string  
        Fav   []string  
}
```

#### 组合

组合是另一种替代继承的方法. 相比于继承的A-is-a-B的关系, 组合则是A-uses-B或者A-has-a-B的关系.

```{code} cpp
:linenos:
:filename: stack.cpp
:emphasize-lines: 13
:caption: 这里stack和vector虽然在内存表达上是相同的, 但概念上stack和vector还是有所不同的. 所以Stack is A Vector是站不住脚的, Stack Uses Vector或者Stack has A Vector比较合适.

#include <vector>

template <typename T>
class StackByInherit : public std::vector<T> {
public:
    void append(T val);
    T pop();
};

template <typename T>
class StackByComposite {
private:
    std::vector<T> _data; // stack-has-a-vector
public:
    void append(T val);
    T pop();
};

```

## 使用OOP的最佳实践

那么，什么时候使用OOP，怎样使用OOP才是最佳实践？

### 经典参考材料

早在上世纪90年代，许多经验丰富的开发者就提出了基于OOP的设计原则和设计模式。相关资料繁多，这里列举一些经典材料.

- [Design Pattern for Humans](https://github.com/kamranahmedse/design-patterns-for-humans)
- [敏捷软件开发](https://book.douban.com/subject/1140457/)
- [软件设计的哲学](https://book.douban.com/subject/37119755/)
- [重构:改善既有代码的设计](https://book.douban.com/subject/30468597/)

---

| Category     | Name                                 | Description                                                                |
| :----------- | :----------------------------------- | :------------------------------------------------------------------------- |
| **设计模式** | 单例模式 (Singleton)                 | 确保一个类只有一个实例，并提供全局访问点。                                 |
|              | 工厂模式 (Factory)                   | 定义一个创建对象的接口，让子类决定实例化哪一个类。                         |
|              | 抽象工厂模式 (Abstract Factory)      | 提供一个创建一系列相关或相互依赖对象的接口。                               |
|              | 观察者模式 (Observer)                | 定义对象间的一种一对多依赖关系，当一个对象改变时，所有依赖者都会收到通知。 |
|              | 代理模式 (Proxy)                     | 为其他对象提供一种代理以控制对这个对象的访问。                             |
|              | 装饰器模式 (Decorator)               | 动态地给对象添加额外的职责。                                               |
|              | 策略模式 (Strategy)                  | 定义一系列算法，封装起来，使它们可以互换。                                 |
|              | 适配器模式 (Adapter)                 | 将一个类的接口转换成客户希望的另一个接口。                                 |
|              | 责任链模式 (Chain of Responsibility) | 使多个对象都有机会处理请求，避免请求的发送者和接收者耦合。                 |
|              | 命令模式 (Command)                   | 将请求封装成对象，从而使你可用不同的请求对客户进行参数化。                 |
|              | 状态模式 (State)                     | 允许对象在内部状态改变时改变行为。                                         |
|              | 备忘录模式 (Memento)                 | 在不破坏封装性的前提下，捕获一个对象的内部状态。                           |
|              | 迭代器模式 (Iterator)                | 提供一种方法顺序访问一个集合对象中的各个元素。                             |
|              | 组合模式 (Composite)                 | 将对象组合成树形结构以表示“部分-整体”的层次结构。                          |
| **设计原则** | 单一职责原则 (SRP)                   | 一个类只负责一项职责。                                                     |
|              | 开闭原则 (OCP)                       | 软件实体应对扩展开放，对修改关闭。                                         |
|              | 里氏替换原则 (LSP)                   | 子类对象能够替换父类对象且程序行为不变。                                   |
|              | 依赖倒置原则 (DIP)                   | 高层模块不应该依赖底层模块，二者都应该依赖抽象。                           |
|              | 接口隔离原则 (ISP)                   | 不应强迫客户依赖它们不使用的方法。                                         |
|              | 迪米特法则 (LoD)                     | 一个对象应对其他对象有尽可能少的了解。                                     |
|              | 合成复用原则 (CRP)                   | 优先使用对象组合，而不是继承来达到复用目的。                               |

---

不过，有几点需要说明：

首先，设计模式诞生于OOP被滥用的年代，随着技术进步，部分设计模式已不再依赖OOP特性。例如template method模式，由于现代语言中函数普遍为一等公民，高阶函数能够轻松实现template method的功能。

其次，许多设计模式内核相似，表明设计模式存在一定冗余。例如Adapter、Composite、Facade模式，均是在原有类基础上封装并提供一组特定接口, 以达到某种目的。

`设计模式和设计原则的意义在于启发我们编写更优质的代码，而非必须遵守的教条，更不可盲目使用。若无必要理由，使用任何设计模式都可能徒增复杂度`。

设计模式和原则为我们提供了丰富的经验和启发，但它们均建立在确定采用OOP的前提下。由于OOP表现力强大，且有时过于复杂，`很多情况下我们并不需要如此强的表现力，简单模型往往足够`。

### 使用OOP的必要条件

什么时候需要使用类和对象呢？

-  首先，你至少需要暴露一组相关的方法作为API，且方法数量多于一个。
-  其次，需要实例化对象，即对象携带状态，且需要多个不同状态的对象来满足需求。

这两点是使用OOP的最低标准。`如果需求不满足这两点，应优先考虑更简单的模型`。例如，当仅需暴露一组无状态函数时，不妨使用module而非class。

### 真实项目中OOP的三种使用风格

实战中，OOP会引出三种明确的使用风格。

#### 第一种：Data Driven Design

这种风格将类视为数据模型的类型，例如`Account`类，包含`id`、`昵称`、`权限`、`余额`等数据字段。此类对象主要作为数据容器在系统中传递。由于重点在承载数据，类上通常没有方法，或者仅有少量与序列化/反序列化、数据校验和存取相关的方法。使用这些数据类时，常通过组合实现，比如`User`类组合`Account`类。

```{code} python
:linenos:
:filename: data_driven_design.py
:emphasize-lines: 16,19

from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int

@dataclass
class Status:
    healthy: bool
    wealthy: bool
    
@dataclass
class Account:
    id: int
    owner: User
    priority: int
    balance: float
    status: Status

    def marshal(self):
        # 序列化方法
        ...

    def validate(self):
        # 数据校验方法
        ...
```

`数据类通常作为底层依赖被整个系统使用，设计时需格外谨慎`。数据类的设计应对应业务逻辑，随着业务发展，数据类型定义会缓慢演变，`此时需做出合理预测，并用通用方式进行扩展或修改`。

#### 第二种：Responsibility Driven Design

此风格`将类视为行为的实体表现`。设计时优先考虑行为，必要时定义简洁通用的interface或trait。`这种类通常承载少量数据，且数据多为配置参数`。`适用于实现各种行为和工具类`，命名通常暗示功能，如`formatter`、`loader`、`event_handler`、`coordinator`、`ApiFetcher`等。

接口较为稳定，为满足不同需求，可能存在多套实现，如`Loader`接口实现`JsonLoader`、`TomlLoader`等。此风格偶尔使用继承。

这种类非常适合作为模块入口类，如此一来模块暴露的就不是一组函数，而是暴露一个类。

```{code} java
:linenos:
:filename: responsibilityDrivenDesign.java
:caption: 上述例子中的类刻画各种Render行为

package examples.oop;

// Stub classes for missing types
class Shape {}
class Color {}
class Style {}

interface Render {
    void render(Shape s);
    void renderAll(Shape[] s);
}

class GUIRenderer implements Render {
    Color color_;
    Style style_;

    public void render(Shape s) { /* Implementation here */ }

    public void renderAll(Shape[] s) { /* Implementation here */ }
}

class PNGRenderer implements Render {
    Color color_;
    Style style_;

    public void render(Shape s) { /* Implementation here */ }

    public void renderAll(Shape[] s) { /* Implementation here */ }
}
```

#### 第三种：Domain Driven Design (DDD)

`DDD风格的类主要刻画业务逻辑中的核心概念`。目标是描述一组相互协作的概念，`将语言扩展为领域专有语言(DSL)`。\
根据论文[《notable design patterns for domain-specific languages》](https://www2.dmst.aueb.gr/dds/pubs/jrnl/2000-JSS-DSLPatterns/html/dslpat.pdf)，这属于DSL领域中名为“language extension”的设计模式。

DDD风格的类`兼具Data Driven和Responsibility Driven的特点`，既承载数据，又抽象行为，并与系统中其他类型互动。

例如足球游戏中的`player`, `Team`, `Goal`类：

```{code} python
:linenos:
:filename: soccer.py
:caption: Player, Team, Goal为游戏核心对象, 通过它们的互相协作编织游戏主题逻辑

class Player:
    def __init__(self, player_id, name, position, team):
        self.player_id = player_id
        self.name = name
        self.position = position
        self.team = team
        self.has_ball = False

    def pass_ball(self, receiver):
        if not self.has_ball:
            raise Exception(f"{self.name} does not have the ball to pass.")
        if receiver not in self.team.players:
            raise Exception(f"{receiver.name} is not a teammate.")
        self.has_ball = False
        receiver.receive_ball()
        print(f"{self.name} passed the ball to {receiver.name}.")

    def shoot(self, goal):
        if not self.has_ball:
            raise Exception(f"{self.name} cannot shoot without the ball.")
        # Domain rule: maybe check shooting position or stamina here
        self.has_ball = False
        goal.attempt_shot(self)
        print(f"{self.name} shoots at goal!")

    def intercept(self, opponent):
        # Domain rule: only if opponent has ball
        if not opponent.has_ball:
            raise Exception(f"{opponent.name} does not have the ball to intercept.")
        # Successful intercept logic could be probabilistic or based on stats
        success = True  # Simplified here
        if success:
            opponent.has_ball = False
            self.has_ball = True
            print(f"{self.name} intercepted the ball from {opponent.name}.")
        else:
            print(f"{self.name} failed to intercept the ball.")

    def receive_ball(self):
        self.has_ball = True

    def replace(self, substitute):
        if substitute.team != self.team:
            raise Exception("Substitute must be from the same team.")
        self.team.replace_player(self, substitute)
        print(f"{self.name} replaced by {substitute.name}.")

class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = players  # List of Player objects

    def team_mates(self, player):
        return [p for p in self.players if p != player]

    def replace_player(self, current_player, substitute):
        if current_player not in self.players:
            raise Exception(f"{current_player.name} is not in the team.")
        self.players.remove(current_player)
        self.players.append(substitute)

class Goal:
    def __init__(self, position):
        self.position = position
        self.goals_scored = 0

    def attempt_shot(self, player):
        # Simplified scoring logic
        scored = True  # Could be probabilistic based on distance, skill, etc.
        if scored:
            self.goals_scored += 1
            print(f"Goal scored by {player.name}!")
        else:
            print(f"{player.name}'s shot missed.")

team_a = Team("Red Warriors", [])
player1 = Player(1, "Alice", "Forward", team_a)
player2 = Player(2, "Bob", "Midfielder", team_a)
team_a.players.extend([player1, player2])

goal = Goal("North End")

player1.receive_ball()
player1.pass_ball(player2)
player2.shoot(goal)
```

`player`提供方法与其他`player`、`ball`、`team`对象互动，同时拥有如队友列表、球员ID、名字等数据。它兼具Data Driven和Responsibility Driven的特点.

在DDD中，若行为为概念独有，无需单独接口/特质(如传球之于球员)；`若行为为多种概念共有，可抽象为接口/特质(如开火之于大炮和枪)`。\
`此风格很少用继承`，因为业务发展导致频繁修改，基于继承的抽象到具体实现不适合频繁变动。同一概念的不同细分对象(如不同国籍球员)也不通过继承实现。

`DDD风格难度最高`，因其既需管理数据(字段较多)，又需与多对象交互(方法众多)。`若无适当约束，类职责易变形，方法数量易膨胀`。若不重新拆分概念(拆成更多类)，系统演进中易产生超级类。

同时业务逻辑多样，核心概念各异，这种类的定义`无固定套路`。

尽管实现难度大，优质DDD设计绝对是系统`核心价值`之一。

#### 三种风格的配合使用

上述三种类风格常配合使用。

- 数据类作为底层依赖被系统各模块引用，甚至出入系统边界(如数据库、网络请求、文件写入)
- Responsibility Driven风格类作为工具类或模块入口类
- 具体业务逻辑由DDD类穿针引线构建。

::::{tab-set}

以足球游戏为例

:::{tab-item} Data Driven Design
```{code} java
:linenos:
:caption: 承载重要数据被各种地方引用

// 球员能力数据
class PlayerCapacity {
    player_id: string

    speed: float
    passing_skill: float
    organizing_skill: float
    leadership: float
    strength: float
    stamina: float
}

// 比赛表现记录数据
class PerformanceRecord {
    competition_id: string
    player_id: string
    date: datetime
    
    goal: int
    assistance: int
    foul: int   
    playing_second: float
}

// 从json中读入球员能力数据
load(JSON) -> PlayerCapacity

// 从数据库中搜索比赛表现记录
query(player_id, date) -> PerformanceRecord
```
:::

:::{tab-item} Responsibility Driven Design
```{code} java
:linenos:
:caption: 封装某种业务计算或业务行为

// 根据比赛数据更新球员能力
class CapacityUpdater {
    constructor(PlayerCapacity);

    update_by(PerformanceRecord[] records) -> Self
    update_by(PerformaceRecord record) -> Self
    get_capacity() -> PlayerCapacity
}

new_capacity = CapacityUpdater(capacity)
                .update_by(last_year_records)
                .update_by(latest_record)
                .get_capacity()
```
:::

:::{tab-item} Domain Driven Design
```{code} java
:linenos:
:caption: 对业务逻辑进行概念提取, 并抽象成类

// 球员状态机, 球员的状态切换靠他实现
class PlayerFSM {
    capacity: PlayerCapacity;
    state: PlayerState;

    proceed(Action) -> PlayerState
}

// 球员类, 比赛控制靠他实现
class Player {
    team_mates: Player[];
    FSM: PlayerFSM;

    pass(Player) -> void
    shoot(Goal) -> void
    intercept(Player) -> void
    holding_ball() -> bool
    current_state() -> PlayerState

    enum Action {
        PASS, SHOOT, HOLD, INTERCEPT
    }
}
```
:::
::::

这三种类风格既非教条，也无明确界限，更像是业界多年实践总结的规律。基于第一性原理，`开发时应根据自身需求灵活调配使用`。

---

[^software-evolution]: 原文pdf在本文github repo中的`papers/`路径下