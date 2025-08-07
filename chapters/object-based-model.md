# Object Based Model

但对一些应用而言, modular model能力稍显不够. 我们需要更强的模型.

## Object和Module的不同

比起module, object不仅能够承载状态变量, 还能够实例化, 也就是说可以存在多个object, 它们彼此独立, 虽然API相同, 但拥有不同的状态.

对象之所以能力更强, 是因为它可以模拟各种其他实体. 

- 对象拥有一套相关的方法(函数), 并能够隐藏或暴露这些方法, 因此可以当作模块
- 对象承载数据, 因此可以当作数据容器
- 对象可以实现一些特殊方法, {abbr}`使得自身可以被调用(譬如__call__方法, 或者k括号算符)`, 因此可以当作函数被调用
- 对象可以和其他类型的变量协作, 因此可以把对象作为一种新类型的实例.

:::{figure} ../material/all-object.png
无外乎很多语言把一切皆对象作为自己的设计哲学之一.
:::

对象模式风靡后, 有两种不同风格的模型, 一种是{abbr}`Object based programming(基于对象编程模型)`, 一种是{abbr}`Object oriented programming(面向对象编程模型)`.
有{abbr}`相当一部份语言(譬如javascript, lua, Self, smalltalk)`, 选择了object based model来构建自己的对象体系.

## 对象的本质: 如何在任何语言中创造对象

基于对象编程是一种理念, 在不支持对象的语言中, 也可以自己实现对象. 

只要语言中有map, 函数是第一类公民, 并支持闭包, 我们就可以造出对象, 譬如

```{code} python
:linenos:
:filename: hand_made_object.py
:emphasize-lines: 14-18
:caption: 我们把公有数据放在map中, 把私有数据藏在函数闭包中, 只能通过对象暴露的方法进行访问. 每个对象为一个独立的map, 对象上可以访问的方法即为公有方法, 在闭包中未暴露的方法即为私有方法. 通过这种方式, 我们可以在任意语言中定义对象.

def create_obj():
    value = 1
    id_ = 2
    greeting = "hello"
    
    def set_value(new_value):
        nonlocal value
        value = new_value
        ...

    def show():
        print(f"{id_}:{value}")

    return {
        "set_value": set_value,
        "show": show,
        "greeting": greeting
    }

obj = create_obj()

obj["show"]()
obj["set_value"](10)
obj["show"]()
print(obj["greeting"])
```

上面例子中, 对象的主体是一个map(一个key-value容器). map是动态的ADT, 我们也可以使用静态的数据结构(譬如结构体)实现同样的功能.

## 从函数到方法

对象实例中的函数和对象外的普通函数有些微区别. 

::::{tab-set}
如果我们有一个对象实例`book`, 以及一个函数`read(Book)->string`, 该函数读取book对象中的数据, 并返回字符串. 

:::{tab-item} 对象+函数
如果read是一个普通函数和Book对象分离,

调用时我们需要单独获取`read`和`book`, 并调用`read(book)`
:::

:::{tab-item} 把函数放入对象中
如果我们把`read`{abbr}`作为数据(函数也是第一类公民, 也可以被当成数据传递)`, 放入对象`book`中,

调用时我们需要获取`book`对象, 然后调用`book.read(book)`.\
之所以如此, 是因为此时`read`只是一个普通函数, 这样的代码看起来有些冗余.
:::

:::{tab-item} 将函数改为方法
对象中的函数使用起来并不方便. 为了让其使用起来更自然, 大部分语言都提供了语法糖, 让当前函数能够自然的访问对象.

在这个例子中, 为了让`read`能够**自然的**访问`book`, 不同语言给出如下优化:

- 如果用python实现, read会被写作`def read(self): ...`, 其中`self`即当前的`book`对象. 调用时仅需要`book.read()`即可.
- 如果用java实现, read会被写作`String read() {...}`, 我们可以在函数体中使用`this`访问当前的`book`对象. 调用时仅需要`book.read()`即可.
    - 有时我们甚至可以省略`this`, 直接取用book中的数据, `book.read()`可以视为"{underline}`在book的上下文中调用read函数`"

`能够自动获取自身实例对象的函数`, 我们称为方法. 换句话说, 方法就是`上下文绑定在对象上`的函数.
::::

然而不同语言中, 方法和对象的绑定也有不同的风格. 

在大部份语言中, 方法和对象是静态绑定的, 即无论方法被如何传递, 它的self / this始终指向原对象. 

但在一部份语言中, 譬如javascript, 方法和对象的绑定是在调用时进行的, 调用方式不同, 绑定的对象也不同, 这种风格被称为动态绑定.

::::{tab-set}

:::{tab-item} 静态绑定

```{code} python
:linenos:
:filename: static_binding.py
:emphasize-lines: 10,14
:caption: 无论t.show被转存到哪里, 函数始终绑定了对象t作为上下文

class T:
    def __init__(self, val):
        self.val = val

    def show(self):
        print(self.val)


t = T(10)
method = t.show  # 将t.show方法转存到method中

# 调用method等同于调用t.show
# 换句话说method函数依然绑定了t作为上下文!
method()  # 10   

t.val = 5
method()  # 5
```

:::

:::{tab-item} 动态绑定

```{code} javascript
:linenos:
:filename: dynamic_binding.js
:emphasize-lines: 8, 10, 12, 13
:caption: 只有`调用时才确定自己绑定在了哪个对象上`

obj = {
    val: 5,
    show: function() {
        console.log(this.val);
    }
}

// 在这种调用方式下, show知道自己在obj的上下文中执行
obj.show() // 5

// 转存之后, 只有函数show被转存
let method = obj.show

// 在这种调用方式下, method认为自己没有绑定任何对象做上下文
method()  // undefined

// 通过这种方法强制绑定obj作为上下文, 才能正确执行
method.bind(obj)() // 5
```

:::

::::

## 如何构造对象

OOP和Object based model最大的区别在于对象的创建上. 在objects based model中, 我们没有类去创造对象, 我们只能通过其他操作来创建对象. 大体上有5种创建对象的方式.

```{code} javascript
:linenos:
:filename: create_obj.js

// 字面量声明对象
hp = {
  name: "Harry Potter",
  occupation: "wizard",
  level: 5,
  speak: function() { ... }
}

// 使用函数直接组装对象
function person1(name, occupation, level) {
  return {
    name: name,
    occupation: occupation,
    level: level,
    speak: function() { ... }
  }
}
tom = person1("Tom Riddle", "wizard", 100);

// 定义初始化函数, 初始化一个空对象
function person2(name, occupation, level) {
  this.name = name;
  this.occupation = occupation;
  this.level = level;
  this.speak = function() {
    ...
  };
}
newton = new person2("Isac Newton", "scientist", 1000);

// 直接深度复制一个对象, 但无法复制函数, 无法处理循环引用!
function clone(obj) {
  return JSON.parse(JSON.stringify(obj))
}
newton_clone = clone(newton)

// 设置一个对象为原形. 通过这种方式去创建对象. 
newton_derivative = {}
Object.setPrototypeOf(newton_derivative, newton)
// same as Object.create(newton)

```

最后一种构造对象的方式--`通过链接原型构造对象`--是object based model的精髓. 

:::{figure} ../material/create-by-prototype.png
不同于深度复制数据来构造新对象, 我们可以创造一个新对象去引用原有对象. 如果访问到本对象中没有的属性, 就去这个被引用的对象中去找, 我们把这个被引用的对象称为{abbr}`原型(prototype)`.
:::

原型是对象的一个特殊属性, 每个对象都拥有原型. 在其他语言中原型有其他的名字, 譬如在lua中它被叫做meta-table.

## 原型链的实践

既然每个对象都有原型, 那么作为原型的对象也有其原型. 如此一来就有了原型链一说. 一般而言, 原形链用来表示一个对象从具体到抽象的整个链条. 

:::{figure} ../material/prototype-chain.png
譬如这里从wizard到Object由原型链穿起来. 每一个对象都有自己的属性和方法, 而wizard能够访问所有的属性和方法. 譬如`wizard.eat()`, `wizard.del()`.
:::

Object based model和OOP的主要区别就在于原型链. 原型链带来一种特殊的应用模式.

### 从原型创建对象

OOP中一个class创建对象. object-based model则可以从原型创建对象, 这里原型的作用就像是对象模板. 我们只需要创建一个空对象, 其原型指向模版对象即可. 新的属性和方法只需要增加在空对象中, 同名属性和方法会自动覆盖原型中的属性和方法.

:::{figure} ../material/practice-of-prototype-chain.png
譬如这里Harry Potter是这样一个对象
```{code} javascript
{level: 10, scar: "⚡", id:0, .proto:wizard}
```
:::

### 模仿类的继承

既然原型作为对象模版, 模仿了类的作用, 它应该也有办法模仿继承. 

:::{figure} ../material/practice-of-prototype-chain.png
这里, wizard对象就是human对象所谓的“子类型“.
:::


```{code} javascript
:linenos:
:caption: 有趣的是, 以human作为原型, 我们可以创建Issac Newton这个"实例", 同样的以human作为原型, 我们可以创建wizard这个"子类型". `他们有同样的形式`. 
const IssacNewton = {
  iq: 200,
  .proto: human
}

const wizard = {
  MP: 0,
  cast_spell: function(){...},
  .proto: human
}
```

也就是说原型机制用同样的方式表示对象和子类型, `它统一了创建实例和继承`, 这跟OOP是非常不同的.

### 黑魔法: 运行时修改原型

既然原型是对象, 我们就可以在运行时修改它.

:::{figure} ../material/change-prototype-on-the-fly.png
譬如我们可以在运行时把human的原型指向immortal. 这样所有人就突然丢失了eat()和drink(). 我们也可以在thing上增加更多的通用属性和方法.
:::

只需一个简单的改动，所有“被原型”对象的行为都会随之改变。

这种机制极为强大，甚至可视为元编程的一种实践。使用得当时，确实能够大幅减少代码量，但代价是使代码变得难以理解，因此需谨慎使用。
