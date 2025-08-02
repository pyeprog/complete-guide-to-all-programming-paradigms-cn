# Meta Programming

![[Think 2025-06-24 12.01.32.excalidraw]]
最后要介绍的是meta programming. 这个模型的核心理念是代码即数据. 而这个理念冯诺伊曼早在1946年就已经提出. 并且冯诺伊曼机也是按照这个理念设计的. 因此针对meta programming的应用实际上很早就有了.

## Meta Programming的不同含义

根据《Meta-Programming and Model-Driven Meta-Programming Development》这本书, “meta-programming”其实代表很多不同的应用方向.
![[Pasted Image 20250522221530_002.png]]
第一个应用方向是transformation, 程序接受一种语言的源码, 并把它改写成另一种语言. 例如typescript改写成javascript, python2改写为python3, C with class(c++前身)改写为C.

其次是generation, 程序接受一种说明文件(spec), 然后把它改写成程序. 譬如JIT根据字节码创造机器码, Yacc根据语法描述, 生成parser, compiler根据源码生成机器码等等. 这种应用把代码分成了不同的抽象层级.

以上是异质meta programming(heterogeneous meta-programming), 即meta程序和应用程序不是用同一种语言编写的.
后面要介绍的meta programming是同质meta programming(homogeneous meta-programming), 即meta程序和应用程序是同一种语言编写的.

同质化meta programming的一个常见的应用方向是generalization, 即让代码变得更通用, 譬如各种语言中的template系统, 可以用来编写generic数据容器.

```c++
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
    
```

另一个应用方向是编写meta-program. 譬如lisp中提供的macro, c++中template meta programming, 都是在原有应用程序的基础上, 提供了扩展语言, 编译时运行, 动态生成代码等能力.

```lisp
;; Define a macro that creates getter/setter functions
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
(print (get-username))
```

一些框架使用了meta-programming的技巧, 分离关注点, 把业务和框架代码完全隔离. 譬如spring MVC/boot中的应用.

```java
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

另外常见的两种能力是reflection(反射)和meta-data. reflection是在运行时能够获取当前代码结构(譬如类上的结构信息, 函数结构信息, 上下文信息), 甚至修改这些结构和行为, 譬如修改和扩充类定义. 而meta-data则是可以直接把各种文档和描述直接附在程序中, 甚至在runtime下都能直接访问.

```python
import inspect
from functools import wraps

def api_endpoint(method="GET", path="/", description=""):
    """Metadata decorator"""
    def decorator(func):
        func._api_method = method
        func._api_path = path  
        func._api_description = description
        return func

    return decorator

  
class APIController:
    @api_endpoint("GET", "/users", "Get all users")
    def get_users(self):
        return ["user1", "user2"]

    @api_endpoint("POST", "/users", "Create user")
    def create_user(self, data):
        return f"Created: {data}"


# Reflection: inspect and modify at runtime
controller = APIController()

# Access metadata
for name, method in inspect.getmembers(controller, inspect.ismethod):
    if hasattr(method, '_api_path'):
        print(f"{method._api_method} {method._api_path} - {method._api_description}")

# Runtime modification
def new_method(self):
    return "Dynamic method added!"

# Add method dynamically using reflection
setattr(APIController, 'dynamic_endpoint', new_method)
print(f"Added method: {hasattr(controller, 'dynamic_endpoint')}")
```

每一种语言都会提供一种或几种相关的能力.
编译型语言一般支持模版, macro, 提供meta program和generalization. 解释型语言一般支持meta program, 反射和meta-data.

## 什么时候使用meta Programming

什么时候使用meta-programming呢? 需要分情况讨论.

- 异质meta programming在日常工作中用的比较少. 难度偏大. 使用的不是特别频繁.
- 同质meta programming在日常工作中有使用.

其中最常用的是, generalization, reflection, meta-data.

- generalization在实现一些比较通用的算法函数, 容器类的时候会经常使用. 如果是语言是动态类型的, 也就是一个变量可以绑定不同类型的数据, 则一般不会提供这种特性.
- reflection经常被用来做判断. 判断是否对象是某个类的; 获取类的方法列表和数据列表; 获取函数的签名(参数列表和返回值). 而动态构造类, 比较难以驾驭, 因此比较少使用.
- meta-data最常见的用例就是函数, 类, 模块的doc-string. 这几乎成了标配.

编写meta-program相对而言比较不常用, 其中需要再细分.

- template meta programming尽量少用. 很多template meta programming技巧都被用在约束template的类型参数上, 有可能的话使用c++20中的concept是更好的选择.
- macro被用来定义一些宏(代码片段模板), 后续可以利用这些宏来生成代码片段. 这种技巧为例巨大, 容易被反噬. 毕竟一个重要的经验法则是, 如果你不知道是否应该使用meta programming, 那就别用. 如果你真的需要定义宏, 那你一定非常了解所有其他方法都显然不能满足需求, 只有使用macro.

最后, 如果代码库中引入了meta-programming技巧, 则需要大量测试进行覆盖. 升级编译器/解释器版本的时候甚至需要全量测试, 保证业务系统行为不变.
