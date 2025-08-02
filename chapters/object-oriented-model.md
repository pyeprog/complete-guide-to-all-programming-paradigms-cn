# Object Oriented Programming Model

![[Think 2025-06-23 22.58.39.excalidraw]]

虽然大家讨论why OOP sucks的声音不绝于耳, 但OOP仍旧是事实意义上最流行的编程范式. OOP是一种表现力非常强的模型, 而强力的模型提供了各种被误用, 被滥用的方式, 以至于如何用好OOP都成为一门学问. 具体的OOP语法, 相信任何一本OOP语言的书都会介绍, 这里就不再赘述了. 这里我们集中讨论OOP中的重要feature和最佳实践.

## 为什么OOP流行

OOP之所以流行, 是因为

- OOP符合人类的直觉, 本体隐喻是人类赖以生存的隐喻系统的一部份, 而OOP提供了本体隐喻的实践.
- 相比于object-based model, OOP提供了class, 即提供了一个对象蓝图, 让我们可以通过声明式的方式定义对象. 在静态语言中, 这帮助了编译器提升性能. 更重要的是, class引入了更强的约束, 让对象在创建之后不能随意扩展(至少不能很方便的扩展)和修改.
- OOP有很强的模仿能力,
  - 类本身可以被当作type, 我们可以在语言中自己定义type, 并提供type相关的操作符或操作函数
  - 类可以作为一种module, 实际上类和module界限非常模糊, 类本身除开实例化之外的行为和module的行为几乎一模一样. 封装, 访问控制和接口, 一个不差, 甚至比module做的更好.
  - 如果重载了()操作符, 实现了某种内置函数(譬如__call__), 或者实现某些trait或interface, 使得对象能够像函数一样“被调用”. 类中的数据也被保护, 不可被外界访问, 类似于函数的闭包.
- 因为OOP提供了这种相当万能的模仿能力, 它可以用来改造语言, 构造Domain Specific Language, 让其贴近业务逻辑. 这种实践就是Domain Driven Design(DDD)的核心要义.

```python
 as type
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

 as module
class MathUtils:
    PI = 3.14159
    _private_constant = 42

    @staticmethod
    def square(x): return x * x

    @classmethod
    def circle_area(cls, radius): return cls.PI * radius * radius

 as callable
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

- 首先是class风格, 这也是最常见的风格, 我们通过class关键词创造一个class, 可以指定父类来继承, 可以指定interface对象来实现(或继承), 一般都会存在构造函数 / init函数, 以及析构函数. 数据和方法都应在class内.
- struct + impl风格, rust和golang采用这种风格, 在这种风格中, struct首先被定义, 随后通过impl关键词在其上定义方法.
- struct + function风格, 在没有专门支持OOP的语言中, 也有这种风格的OOP. 例如C语言. 在这些语言中, 我们指定定义结构体, 然后定义一组函数, 函数的第一个参数即为结构体对象. 虽然这些函数在没有对象的时候也能被获取, 但需要结构体对象才能正确调用.
![[Think 2025-06-17 22.39.08.excalidraw]]

## OOP的不同性质

OOP在不同的语言中有不同的性质. 我们就以下4种性质进行介绍.

- open class or close class, 在类定义完毕之后还能否往里添加方法.
  - open class的代表, 譬如rust, swift, golang, rust, ruby
  - close class的代表, 大部份class风格的语言.
- method bounded or method unbounded, 方法是否只能通过类或对象获取.
  - method bounded, class风格和struct+impl风格的语言, 它们的方法定义总是跟类绑定
  - method unbounded, struct+function风格的语言, 方法可以单独定义
- inheritance or not, 是否支持继承
  - 绝大部份class风格的语言都支持继承
  - struct+impl风格和struct+function风格的语言, 一般不支持继承. 但它们会提供额外的机制来替代继承.
- interface coerce or not, 类中的方法定义是否能够被接口约束
  - class风格和struct+impl风格一般支持接口约束, golang除外
  - struct+function风格一般不支持接口约束.

 ![[Think 2025-06-18 08.19.59.excalidraw]]
任何一门OOP语言, 一般都在这些风格和性质中组合出自己的OOP风格.

## 继承

在介绍OOP的实践之前, 我们需要先展开说明继承这个特性. 这里提到的继承特指具体类之间的继承(inheritance), 不是继承接口或虚基类(subtyping).
继承是目前OOP被诟病较多的特性, 很多语言公开抛弃继承特性. 大家谈到继承的时候一般会诟病的点是

- 多继承引入了不必要的复杂性
- 继承即耦合, 子类和基类耦合在一起, 基类的改动可能导致子类行为改变甚至错误.
这些诟病的点, 都是确有其事.
一些语言摒弃了多继承抛弃, 另一些引入了额外的特性去解决问题(虚继承). 但耦合仍旧是继承机制避不开的问题.

### 继承为什么被诟病

但仍旧有海量语言仍旧实现了继承的特性. 为什么继承这么垃圾, 还要坚持支持继承呢? 其中的问题到底出在哪里呢?
首先继承诞生的前提是非常合理的. 在引入类和对象之后, 人们观察到了大量的重复代码, 不同的类想要实现同样的方法, 要么复制粘贴一份, 这增加了代码冗余度; 要么就要把方法抽到类的外面, 而这回到了struct+function风格, 破坏了封装. 为了减少代码重复同时保护封装, 才发明了继承.

引入继承的原始动机也非常合理. 有了继承, 我们可以进行先抽象再具体的编码. 譬如Object > Creature > Animal > Mammal > human, 层层递进, 一气呵成, 十分符合逻辑. 第二个动机是, 当时的人们想要对系统进行扩展, 但新需求进来的时候, 不需要实现新的类, 只需要继承原有类并实现一个子类即可. 而这是符合开闭原则的实践.

继承诞生的前提无可挑剔, 动机也非常合理. 但问题出在假设上.
先抽象再具体的编码假设一开始架构师就能够正确理解业务问题, 对业务未来的走向了熟于心, 并对问题进行正确的抽象. 只有这样, 基类才能提供真正有用的方法和属性, 完美贴合业务问题的方方面面, 在未来也不需要修改. 只有这样耦合原有实现才不会导致问题.
而这个假设是站不住脚的. 很多文章, 书籍, 论文都说明过, 再优秀的业务分析(Business Analysis)也无法完全洞悉客户的需求, 客户的需求会随着交付的系统而流变. 再优秀的架构师也无法作出永远合适的抽象模型, 因为需求在缓慢变化, 总有一天原来的抽象会不再适用. **Laws of Software Evolution Revisited**这篇论文中提到, 系统必须不断的修改和适应用户不断流变的需求, 一旦停止适应, 用户会明显感受到系统的劣化, 甚至会因此弃用. 就算当下的需求被完美适配了, 但系统总会在未来某个时间点变得不再满足需求了.
如果在需要修改的时候才发现过去和现在已经通过继承完美的耦合起来了, 基类改不得, 继续继承写不动. 走到这一步, 系统就已经走完了它短暂的一生, 很可能最终的结局是重写系统.

### 什么时候使用继承

所以我们要完全抛弃继承吗? 也不见得.
如果两个类是Is-A关系, 使用继承就是合适的. 譬如cat is a critter. 那么cat类继承于critter类就是合适的.
具体而言, 先抽象再具体的编码, 在一些场合是合适使用继承的. 譬如业务无关的稳定概念就很适合使用继承. shape > rectangle > square就是一个几何领域一个很好的例子.
人们想要通过继承的方式对系统进行扩展, 这本身没有问题, 只要继承的不是具体类, 而是稳定的interface / trait. 这样所有的实现只和稳定的api耦合, 同时满足开闭原则和依赖反转原则. 通常这不叫继承(inheritance), 而叫做创建子类型(subtyping).

综上, 如果使用继承, 则我们应该谨慎的, 小范围的使用继承, 只有继承能够极大简化实现的时候使用. 跨模块的继承是绝对要避免的, 不必要时完全可以用组合, 代理, 甚至函数式编程代替.

### 代替继承

#### 委托

委托(代理)是代替继承的另一种机制. 类似于object based model中对象可以把数据或函数的请求委托给自己的原形. 在OOP中也存在类似的机制.

```go
type Animal struct {  
        Kingdom string  
        Legs    uint8}
type Cat struct {  
        Animal  
        Sound string  
        Fav   []string  
}
```

这里Cat把Legs和Kingdom委托给Animal. 我们可以直接在Cat的实例中访问这两个属性.

#### 组合

组合是另一种替代继承的方法. 相比于继承的A is a B的关系, 组合则是A uses B或者A has a B的关系.

```c++
template <typename T>
class StackByInherit : public std::vector<T> {
public:
 void append(T val);
 T pop();
}

template <typename T>
class StackByComposite {
private:
 _data = std::vector<T>()
public:
 void append(T val);
 T pop();
}
```

譬如上面例子中StackByComposite就是使用了组合的方式. 这里stack和vector虽然在内存表达上是相同的, 但概念上stack和vector还是有所不同的. 所以Stack is A Vector是站不住脚的, Stack Uses Vector或者Stack has A Vector比较合适.

## 使用OOP的最佳实践

那么, 什么时候使用OOP, 怎样使用OOP才是最佳实践?
早在上世纪90年代, 就有很多经验丰富的开发者提出了基于OOP上的设计原则和设计模式. 相关的材料已经数不胜数, 我这里就不再赘述.
![[Think 2025-06-18 22.22.51.excalidraw]]

### 经典原则

| 原则     | 含义                                    |
| ------ | ------------------------------------- |
| 单一职责原则 | 一个函数/类/模块, 做一件(一类)事情                  |
| 开闭原则   | 程序应该设计的对修改关闭, 对扩展开放, aka, 设计良好的接口     |
| 里氏替换原则 | 子类应该方法输入应该更宽松, 输出应该更严格                |
| 接口隔离原则 | 接口(interface)应该做好关注点分离, 每套接口都服务于一致的目的 |
| 依赖反转原则 | 使用良好稳定的接口来确定模块行为, 放置修改在模块内外传播         |
![[Pasted image 20250609153929.png]]

但是, 有几点需要说明.
首先, 设计模式诞生于OOP被滥用的年代, 随着技术的进步, 一部份设计模式已经不再依赖OOP特性. 譬如template method模式, 因为现在的语言中, 函数普遍是一类公民, 所以高阶函数能够轻松完成template method所做的工作.
另外, 很多设计模式其实内核非常相似, 说明设计模式也有不少冗余. 譬如Adapter, Composite, Facade模式, 它们都在原有类的基础上, 提供一组特定的接口.
设计模式和设计原则存在的意义是启发我们写出更好的代码, 而不是某种必须遵守的教条. 更不能盲目使用. 如果没有必要的理由, 使用任何一种模式都是徒增复杂度.

设计模式和原则给我们提供相当多的启发和经验, 但他们都是在确定使用OOP的前提下才能成立. 因为OOP表现力很强, 很多时候表现力过强, 我们并不需要, 很多时候我们只需要更简单的模型即可.

### 使用OOP的必要条件

什么时候需要使用到类和对象呢?

- 首先你至少需要暴露一组相关的方法作为api, 方法数量大于1个.
- 其次, 我们需要实例化的对象, 即对象携带状态, 而我们需要若干不同状态的对象实现需求.
这两点是使用OOP的最低标准. 如果需求达不到这两点要求, 就应该使用更简单的模型. 譬如当我需要暴露一组无状态的函数时, 不妨考虑使用module而不是class.

### 真实项目中OOP的三种使用风格

实战中, OOP会引出三种明确的使用风格.
第一种, data driven design. 这种风格把类当作数据模型的type, 譬如Account, 就需要有id, 昵称, 权限, 余额等等数据字段. 这种类的对象会作为数据容器被传递到整个系统中. 因为主要使用它承载数据, 所以类上没有任何方法, 或者只有少量方法, 所有方法都只和序列化/反序列化, 数据校验和存取有关. 譬如Account和相关方法会这样实现. 在使用这些数据类时, 我们几乎总是使用组合, 譬如使用User类去组合Account类.
![[Think 2025-06-18 22.35.03.excalidraw]]
数据类一般会作为底层依赖被整个系统使用, 因此设计的时候需要万分谨慎. 数据类在设计的时候也要对应业务逻辑, 随着业务的发展, 数据类型的定义也会慢慢流变, 此时我们需要做出正确的预测, 并用较为通用的方式进行扩展或修改.
如果我有一个数据类Account, 主要承载账户相关的数据, 之前公司主要做消费者业务, 因此账户都是个人账户, 现在公司开始做企业服务业务, 因此需要在系统中加入企业账户, 你会怎样设计呢?
![[Think 2025-07-11 20.55.52.excalidraw]]

第二种, responsibility driven design. 这种风格把类当作行为的实体表现. 在设计这种类之前优先考虑其行为, 并定义简洁通用的interface / trait. 这种类可能承载少量的数据, 且定义的数据一般是某种配置参数. 我们用这种风格实现各种行为和工具类. 它们的命名暗示它们的功能, 譬如formatter, loader, event_handler, coordinator, ApiFetcher等等.
它们的interface / trait比较稳定, 而且为了应对不同的需求, 有可能会有许多套实现, 譬如JsonLoader, TomlLoader等等. 这类风格偶尔会用到继承.
这种风格的类非常适合作为模块的入口类. 即模块不用暴露一组函数, 而是暴露一个类即可.
![[Think 2025-06-18 23.03.12.excalidraw]]

第三种, domain driven design(DDD). 这种风格的类主要对业务逻辑中的核心概念进行刻画. 使用这种风格的主要目的是刻画一组能够相互协作的概念, 把语言扩展为领域专有语言(DSL). 根据《notable design patterns for domain-specific languages》这篇论文, 在DSL领域这是一种被称为“language extension”的设计模式.

在DDD风格中, 类同时具有data driven design和responsibility driven design的风格, 既需要承载数据, 又需要抽象行为, 并且和系统中其他类型有互动.
譬如在足球游戏中, 会有player类.

```python
player.pass(team_mate_player)
player.shoot(goal0)
player.intercept(other_player)
player.has_ball()
player.team_mates()
player.replace(team_mate_player)
```

player提供这些方法, 和其他player, ball, team对象进行互动. player上也有数据, 譬如队友player的列表, 球员id, 球员名字等等.

DDD风格的类, 如果行为是一种概念独有的, 就不需要单独的interface / trait(譬如传球之于球员), 如果行为是若干种不同的概念共有的, 那么行为也可以抽象成interface / trait(譬如开火之于大炮和枪). 不过, 这个风格的类基本也很少用到继承, 因为业务发展, 这些类也会跟着修改, 基于继承的从抽象到具体的实现方式, 并不适合频繁的修改. 同一种概念的不同细分对象(譬如不同国籍的球员), 也不会通过继承去实现.

这种风格是最难驾驭的风格, 因为它既需要管理数据, 所以有一定数量的数据字段, 又需要和各种其他的对象进行互动, 所以有相当多的方法. 如果没有合适的约束, 类的职责容易变形, 类上的方法数量容易过度膨胀. 这时不去重新调整拆分概念的话(拆分成更多的类), 很容易在接下来系统的演进中变成超级类. 另外, 业务逻辑千千万, 每一种核心概念都不同, 同一种概念刻画角度不同, 类的定义也不同. 并没有一种固定的套路和答案可以参考. 虽然实现难度很高, 但收益也大, 一套好的DDD设计, 的的确确是系统的核心价值之一.

上面提到的三种风格的类, 经常是配合一起使用的. 数据类被系统的各个模块引用, 甚至出入系统边界(入库, 网络请求, 写文件). responsibility driven风格的类, 作为各种工具类, 或者各个模块的入口类. 而具体业务逻辑的实现则由DDD类穿针引线来构建.
![[Think 2025-06-19 16.47.52.excalidraw]]

上面的这三种类风格, 既不是教条, 也没有明确的界限, 而更像是业界多年实践后统计下来的规律. 根据第一性原理, 在开发时, 归根究底我们还是应该根据自己的需求灵活调配风格.
