# 元编程

最后要介绍的是{abbr}`元编程(meta programming)`. 这个模型的核心理念是`代码即数据`. 

“代码即数据”的理念由冯·诺依曼早在1946年提出，冯·诺依曼机的设计也基于这一理念。因此，针对[元编程](https://en.wikipedia.org/wiki/Metaprogramming)的实践实际上由来已久。

:::{image} ../material/meta-programming-meme.png
:::


## Meta Programming的不同含义

根据[^meta-programming-book], "元编程"其实代表很多不同的应用方向.

:::{image} ../material/meta-programming-table.png
:width: 100%
:align: center
:::

### 异质元编程

{abbr}`异质元编程(heterogeneous meta-programming)`, 是指meta程序和应用程序不是用同一种语言编写的.

异质元编程应用方向包括:

- **Transformation**, 即程序接受一种语言的源码, 并把它改写成另一种语言的源码. 例如typescript改写成javascript, python2改写为python3, {abbr}`C with class(c++前身)`改写为C.
- **Generation**, 程序接受一种{abbr}`说明文件(spec文件)`, 然后把它改写成程序. 譬如JIT根据字节码创造机器码, Yacc根据语法描述生成parser, compiler根据源码生成机器码等等. 这种应用把代码分成了不同的抽象层级.

然而除非专门研究语言设计, 异质元编程在日常应用开发中, 我们很少接触. 

### 同质元编程

{abbr}`同质元编程(homogeneous meta-programming)`, 是指meta程序和应用程序是同一种语言编写的.

#### Generalization

同质化元编程的一个常见的应用方向是{abbr}`generalization(代码泛化)`, 即让代码变得更通用, 譬如各种语言中的template系统, 可以用来编写generic数据容器和复杂的算法.

```{code} cpp
:linenos:
:filename: generalization.cpp

#include <cstddef>

template<typename T, size_t N>
class Stack {
private:
	T data[N];
	size_t top = 0;

public:
	void push(const T& item) {
		if (top < N) data[top++] = item;
	}

	T pop() {
		return top > 0 ? data[--top] : T{};
	}

	bool empty() const { return top == 0; }
	size_t size() const { return top; }
};

int main() {
	Stack<int, 10> intStack;
	Stack<float, 20> floatStack;
};
    
```

#### 开发meta-program

同质化元编程另一个应用方向是编写meta-program. 譬如lisp, c, rust等语言中的macro, 都是在原有应用程序的基础上, `提供了扩展语言, 编译时运行, 动态生成代码`等能力.

::::{tab-set}

:::{tab-item} lisp macro
```{code} lisp
:linenos:
:filename: macro.lisp
:caption: 参考[^lisp-book]中的第10章

;; 定义一个宏, 运行后自动生成一个全局变量和它的getter, setter
(defmacro defproperty (name)
  (let ((getter (intern (format nil "GET-~A" name)))
		(setter (intern (format nil "SET-~A" name)))
		(var (intern (format nil "*~A*" name))))

	`(progn
	   (defvar ,var nil)
	   (defun ,getter () ,var)
	   (defun ,setter (value) (setf ,var value)))))

(defproperty username)
(set-username "Alice")
(print (get-username)))
```
:::

:::{tab-item} c macro
```{code} c
:linenos:
:filename: macro.c

#include <stdio.h>

// 定义生成add函数的宏
#define GENERATE_ADD_FUNC(type)       \
type add_##type(type a, type b) {     \
  return a + b;                       \
}

GENERATE_ADD_FUNC(int)
GENERATE_ADD_FUNC(float)

int main() {
  int iresult = add_int(3, 4);
  float fresult = add_float(2.5f, 4.5f);

  printf("int add: %d\n", iresult);
  printf("float add: %.2f\n", fresult);

  return 0;
}
```
:::

:::{tab-item} rust macro
```{code} rust
:linenos:
:filename: macro.rs

// 定义生成add函数的宏
macro_rules! generate_add_fn {
    ($func_name:ident, $t:ty) => {
        fn $func_name(a: $t, b: $t) -> $t {
            a + b
        }
    };
}

generate_add_fn!(add_i32, i32);
generate_add_fn!(add_f64, f64);

fn main() {
    let int_sum = add_i32(3, 4);
    let float_sum = add_f64(2.5, 4.5);

    println!("int add: {}", int_sum);
    println!("float add: {}", float_sum);
}

```
:::
::::

#### 关注点分离

一些框架使用了meta-programming的技巧, 分离关注点, 把业务和框架代码完全隔离. 譬如spring MVC/boot中的应用.

```{code} java
:linenos:
:filename: xController.java
:caption: 在使用spring boot之后, 在代码库中除了注解, 你几乎看不到任何关于spring的代码. 而注解本身没有任何逻辑效用.

@RestController
@RequestMapping("/users")
public class UserController {
    @Autowired
    private UserService userService;

    @GetMapping("/{id}")
    @Cacheable("users")
    public User getUser(@PathVariable Long id) {
        return userService.findById(id);
    }

    @PostMapping
    @Transactional
    @Valid
    public User createUser(@RequestBody User user) {
        return userService.save(user);
    }
}

@Service
@Transactional
public class UserService {
    @Autowired
    private UserRepository repository;

    @Retryable(maxAttempts = 3)
    public User findById(Long id) {
        return repository.findById(id).orElse(null);
    }

    public User save(User user) {
        return repository.save(user);
    }
}
```

#### 反射和元信息

另外常见的两种能力是{abbr}`反射(reflection)`和{abbr}`元信息(meta-data)`. 反射是在运行时能够获取当前代码结构(譬如类上的结构信息, 函数结构信息, 上下文信息), 甚至修改这些结构和行为(譬如修改和扩充类定义). 而元信息是可以直接把各种文档和描述直接附在程序中, 甚至在runtime下都能直接访问.

```{code} python
:linenos:
:filename: dynamicly_load_json.py
:emphasize-lines: 19,26

import json
from dataclasses import dataclass, fields, is_dataclass
from typing import List, get_origin, get_args

@dataclass
class Address:
    street: str
    city: str

@dataclass
class Person:
    name: str
    age: int
    address: Address
    tags: List[str]

# 通用的from_json方法, 使用反射的技巧来动态加载json到dataclass中.
def from_json(cls, json_dict):
    """这里的docstring就是元信息, 你可以通过from_json.__doc__在runtime下得到这些元信息"""

    if not is_dataclass(cls):
        raise TypeError(f"{cls} is not a dataclass")

    init_kwargs = {}
    
    for field in fields(cls):  # 遍历给定class的每一个字段
        field_value = json_dict.get(field.name)

        if field_value is None:
            continue

        field_type = field.type
        origin = get_origin(field_type)

        # 如果字段是嵌套的dataclass, 递归调用from_json进行处理
        if is_dataclass(field_type):
            init_kwargs[field.name] = from_json(field_type, field_value)

        # 如果字段是个list, 尤其是list of dataclasses, 要进行递归处理
        elif origin is list or origin is List:
            item_type = get_args(field_type)[0]
            if is_dataclass(item_type):
                init_kwargs[field.name] = [from_json(item_type, item) for item in field_value]
            else:
                init_kwargs[field.name] = field_value

        else:
            init_kwargs[field.name] = field_value

    return cls(**init_kwargs)

# Example JSON
json_str = '''
{
    "name": "Bob",
    "age": 40,
    "address": {
        "street": "123 Main St",
        "city": "Metropolis"
    },
    "tags": ["friend", "colleague"]
}
'''

data = json.loads(json_str)
person = from_json(Person, data)

# 使用反射遍历person的字段.
for field in fields(person):
    value = getattr(person, field.name)
    print(f"Field: {field.name}, Type: {field.type}, Value: {value}")

```

---

每种语言通常都会提供一种或多种相关能力。

-  **编译型语言**一般支持模板(template)、宏(macro)，以实现元编程(meta programming)和泛化(generalization)。
-  **解释型语言**通常支持元编程、反射（reflection）以及元数据（meta-data）。

## 什么时候使用meta Programming

什么时候使用meta-programming呢？需要分情况讨论。

-  **异质meta programming**在日常工作中使用较少，难度较大，频率不高。
-  **同质meta programming**在日常工作中较为常见。

其中最常用的包括generalization、reflection和meta-data。

-  **Generalization**常用于实现通用算法函数和容器类。如果语言是动态类型（变量可绑定不同类型数据），则通常不会(也不需要)提供这类特性。
-  **Reflection**常用于判断对象类型、获取类的方法和数据列表、获取函数签名（参数列表和返回值）。动态构造类较难掌控，因此较少使用。
-  **Meta-data**最常见的用例是函数、类、模块的doc-string，几乎成为标配。

编写meta-program相对不常用，且需细分：

-  **Template meta programming**应尽量少用。许多技巧用于约束template的类型参数，若可能，C++20中的concept是更优选择。
-  **Macro**用于定义代码片段模板，后续可利用宏生成代码。此技巧影响巨大，也易反噬。经验法则是：如果不确定是否应使用meta programming，就不要使用；若确实需要定义宏，说明你非常了解其他方法无法满足需求，只有宏能解决。

最后，若代码库引入meta-programming技巧，`需大量测试覆盖。升级编译器或解释器版本时，甚至需要全量测试以确保业务系统行为不变`。

---

[^meta-programming-book]: [Meta-Programming and Model-Driven Meta-Programming Development](https://www.amazon.com/Meta-Programming-Model-Driven-Meta-Program-Development-Information/dp/1447141253), 作者 Vytautas Štuikys, Robertas Damaševičius, 2013年出版  
[^lisp-book]: [ANSI Common Lisp](https://book.douban.com/subject/1456906/), 作者 Paul Graham, 1995年出版