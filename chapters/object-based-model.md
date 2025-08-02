# Object-based Model

![[Think 2025-06-23 10.36.41.excalidraw]]
modular model是一种通用的模型, 但对一些应用而言, modular model能力稍显不够.

## Object和module的不同

比起modularity, object能够承载多个状态变量. object还能够实例化, 也就是说可以存在多个object, 它们彼此独立, 拥有不同的状态.
对象之所以能力更强, 是因为它可以模拟各种其他实体. 对象拥有一套相关的方法(函数), 并能够隐藏或暴露这些方法, 因此可以当作模块; 对象承载数据, 因此可以当作数据容器; 对象可以实现__call__方法, 或者()运算符, 因此可以当作函数被调用; 对象可以和其他类型的变量协作, 因此可以把对象作为一种新类型的实例. 无外乎很多语言把一切皆对象作为自己的设计哲学之一.

对象模式风靡后, 有了两种模型, 一种是Object-based model, 一种是Object Oriented Model.
有相当一部份语言包括javascript, lua, Self, small-talk, 选择了Object-based model来构建自己的对象体系.

## 对象的本质: 如何在任何语言中创造对象

基于对象编程是一种理念, 在不支持对象的语言中, 也可以自己实现对象. 只要语言中有map则中ADT, 函数是第一类公民, 以及支持闭包, 我们就可以造出对象, 譬如

```python
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
  "set_value": set_value
  "show": show
  "greeting": greeting
 }

obj = create_obj()

obj["show"]()
obj["set_value"](10)
obj["show"]()
print(obj["greeting"])
```

这个例子中, 我们把公有数据放在map中, 把私有数据藏在函数闭包中, 只能通过对象暴露的方法进行访问. 每个对象相互独立, 对象上可以访问的方法即为公有方法, 在闭包中未暴露的方法即为私有方法. 通过这种方式, 我们可以在任意语言中使用对象模型.

从这个例子中, 我们可以看到对象的主体是一个map. 是一个key-value容器.
Object based model引进了更好的支持. 它引入了record类型. 本质上它仍旧是个map. 但我们可以通过字面量去访问其元素. 譬如在map中, 我们需要`obj["show"]`去访问show方法, 在record中我们只需要`obj.show`即可.
从这里我们可以说, 对象本质上是一个record类型的实例. 其中包含有若干数据和方法.

## 从函数到方法

record实例中包含的数据可以是函数, 因为函数也是第一类公民, 也可以被当成数据传递. 起初, 对象中的函数和对象本身没有任何关系, 我们可以随机放一个函数到对象内, 而函数也不会知道对象的存在, 对象也不会知道里面的函数和其他函数有什么区别. 但我们把数据和函数放在一起的根本目的是让函数可以方便的使用这些数据. 或者说对象是一种上下文, 他给函数隐式的提供了数据.

- `obj.function(obj)`, 如果函数和obj无关, 我们只好如此调用, 来访问obj中的数据
- `obj.function()`, 但是上述调用冗余且丑陋, 我们期望能够这样调用
  - `fn function(self)`, 在函数定义中, 可以显式的把当前对象作为函数第一个参数
  - `fn function()`, 也可以直接在函数体中使用self / this去获取当前对象.

无论显式还是隐式获取self / this, 都把对象和函数绑定在一起. 我们也把这种有绑定的函数称为对象的方法.

然而不同语言中, 方法和对象的绑定也有不同的风格. 在大部份语言中, 方法和对象是静态绑定的, 无论方法被如何传递, 它的self / this始终指向原对象. 但在一部份语言中, 譬如javascript, 方法和对象的绑定实在方法调用时进行的, 调用方式不同, 绑定的对象也不同, 这种风格被称为动态绑定.
![[Think 2025-06-23 16.45.35.excalidraw]]

## 如何构造对象

OOP和Object-based model最大的区别在于对象的创建上. 在object-based model中, 我们没有类去创造对象, 我们只能通过其他操作来创建对象. 大体上有5种创建对象的方式.

```javascript
// 字面量声明对象
hp = {
 name: "Harry Potter",
 occupation: "wizard",
 level: 5,
 speak: function() {...}
}

// 使用函数直接组装对象
function person1(name, occupation, level) {
 return {
  name: name, occupation: occupation, level: level,
  speak: function() {...}
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

// 直接深度复制一个对象
function clone(obj) {
 return JSON.parse(JSON.stringify(obj))
}
newton_clone = clone(newton)

// 设置一个对象为原形. 通过这种方式去创建对象. 
newton_derivative = {}
Object.setPrototypeOf(newton_derivative, newton)
// same as Object.create(newton)
```

前4个都比较好理解. 但最后一个是object-based model的精髓. 不同于深度复制对象来创建新对象. 我们可以创造一个新对象去引用原有对象. 如果访问到本对象中没有的属性, 就去这个被引用的对象中去找, 我们把这个被引用的对象称为原型. 原型是对象的一个特殊属性, 几乎每个对象都拥有原型. 在其他语言中原型有其他的名字, 譬如在lua中它被叫做meta-table.
![[Think 2025-06-23 20.50.34.excalidraw]]

## 原型链的最佳实践

既然每个对象都有原型, 那么作为原型的对象也有其原型. 如此一来就有了原型链一说. 一般而言, 原形链用来表示一个对象从具体到抽象的整个链条. 譬如这里从wizard到Object由原型链穿起来. 每一个对象都有自己的属性和方法, 而wizard能够访问所有的属性和方法. 譬如`wizard.eat()`, `wizard.del()`.
![[Think 2025-06-23 22.24.06.excalidraw]]

Object-based model和OOP的一个主要区别就在于原型链. 这带来一种特殊的应用模式.

### 从原型创建对象

OOP中一个class创建对象. object-based model可以从原型创建对象. 这里原形的作用就像是对象模板. 我们只需要创建一个空对象, 其原型指向模版对象即可. 新的属性和方法只需要增加在空对象中, 同名属性和方法会自动覆盖原型中的属性和方法.
![[Think 2025-06-23 22.38.18.excalidraw]]

### 模仿类的继承

既然原型作为对象模版, 模仿了类的作用, 它应该也有办法模仿继承. 实际上在上一个例子中, wizard这个对象就是human所谓的“子类型“. 有趣的是, 以human作为原型, 我们可以创建Issac Newton这个"实例", 同样的以human作为原型, 我们可以创建wizard这个"子类型". 也就是说原型机制用同样的方式表示对象和子类型, 它统一了创建实例和继承, 这跟OOP是非常不同的.

### 黑魔法: 运行时修改原型

既然原型是对象, 我们就可以在运行时修改. 譬如我们可以在运行时把human的原型指向immortal. 这样所有人都不需要吃喝了. 我们也可以在thing上增加更多的通用属性和方法.
只要一个简单的改动, 所有的对象, 包括牛顿, 哈利和伏地魔都会改变行为.
这种机制过于强大, 可以算是元编程的一种实践, 用得好时确实可以大大减少代码量, 但代价是让代码变得难以理解. 因此需要谨慎使用.
![[Think 2025-06-23 22.51.17.excalidraw]]
