# 显式状态模型

![[Think 2025-06-22 21.06.51.excalidraw]]
接下来让我们进入explicit state显式状态模型中
declarative model中的变量的值是不能修改的, 这被称为不变性, 在这个模型中, 如果我有一个巨大的array, 我想修改它最后一个值, declarative model不得不重新创建一个新的array来满足我的需求. 这肉眼可见的低效. 另外, 因为没有循环关键词, 所以我们不得不使用递归来替代, 这也使得一些特定的程序变得非常难写. 哪怕是像反转array这种简单的功能, 都很难写出高效的版本.

显式状态模型在声明式模型的基础上增加了“可修改的变量”这一重量级feature. 这意味着我们除了能写declarative code -- 通过声明我们想要的结果来写代码, 也可以写imperative code -- 通过声明具体操作来写代码. 而这正是我们最常使用的语言范式.

## 变量在不同语言中的不同风格

虽然变量看起来非常简单, 但不同语言对其有十分不同的阐述.

### 强类型 Vs 弱类型

首先, 你会听到一种说法说某种语言是强类型的, 另一种是弱类型的. 这是什么意思呢? 如果一个语言是弱类型的, 那么意味类型之间可以进行隐式转换, A类型的值可以被当作B类型去使用, 譬如在c语言中, 我只需要用void\*指针指向任意一个值, 就可以把它的类型抹掉, 然后赋给任意一种其他类型的指针. 弱类型总是被作为一种缺点被攻击, 而目前大部份主流语言都是强类型的.
![[Think 2025-06-22 21.17.16.excalidraw]]

### Dynamic Type Vs Static Type

变量是动态的还是静态的? 大部份静态语言都会在声明变量时指定一个类型, 这些语言里, 变量的值可以改变, 但类型都必须跟变量允许的类型一致, 变量类型是静态的. 而在大部份的动态语言中, 变量的类型是动态的, 变量可以被赋予完全不同类型的值.
![[Think 2025-06-22 21.17.32.excalidraw]]

### Pass by Value Vs Pass by Reference

变量作为函数的参数传递时,  我们会说一些语言传参的方式是pass by value, 另一些是pass by reference. 意思是除开基础类型, 对于大部分类型, pass by value会复制变量作为函数实参, 而pass by reference会把变量的引用(也就是不复制, 传的是参数本体)作为函数实参. pass by reference的语言在函数体内修改了变量, 就会改变原有变量.
![[Think 2025-06-16 11.30.46.excalidraw]]

### 标识符是否和值分离

最后, 在一门语言中, 变量的值和标识符是否分离? 这是什么意思呢? 变量的标识符就是变量名. 在大部份语言中, 把变量的标识符放入表达式就等于把值放入表达式. 这一点我们已经十分习惯了. 然而在相当一部份的语言中, 变量的值和标识符是分离的.
![[Think 2025-06-16 11.38.19.excalidraw]]
譬如在OZ这门语言中, 新建变量等于新建一个cell, 而赋值和取值需要使用@操作. cell本身不是变量, 是不能够直接放入表达式的.
![[Pasted image 20250616110745.png]]

换一种角度理解标识符和值的分离, 我们也可以说在一些语言中, 提供了一种数据容器, 容器中承载一个值, 容器中的值可以修改.
为什么我们要费力分离值和标识符? 提供一个类似值容器的东西, 有什么好处吗? 实际上, 还真有好处. 实际上大部份的语言中都有这种值容器, 譬如java中的AtomicInteger, 能让一个整数的读写原子化; clojure中的agent, 能够异步的进行计算并赋值, 类似于其他语言中的future; closure的atom, 除了原子化读写之外, 还可以挂一个校验函数在容器上, 只有通过校验的值才能被覆盖容器内的值; rust中的box和c++中的smart pointer能够管理堆内存的释放, 防止内存泄露; python中的weak_ref能够提供弱引用, 被弱引用的对象其引用计数不增加, 防止两个对象互相引用, 导致gc难以回收. 而在c/c++中, 我们甚至可以把指针看作一种分离值和标识符的容器, 它的作用是能够在内存空间中修改指向的地址, 并且规避复制值带来的开销.
![[Think 2025-06-16 11.09.42.excalidraw]]

总之, 变量的值和标识符不分离, 那么用起来十分简单, 符合直觉.
变量的值和标识符分离, 变量则像一个值容器, 则能取值之上提供额外的功能.

## 引入可修改的变量后的改变

引入可修改的变量之后, 我们可以循环修改变量值. 因此for / while / loop这样的循环关键词随即被引入, 为了更好的控制执行, 随后continue和break也被引入. 最后try catch final被引入用来处理意外的状态或者外部系统的状态引发的异常.
这些语法都只在变量可修改时才有意义.

## 什么时候引入可修改变量

当我们需要写复杂算法时, 尤其是业务相关的算法时, 我们需要复杂的嵌套循环, 甚至循环嵌套递归来实现业务逻辑, 此时就需要使用表现力更强的显式状态, 一边循环一边修改变量值.
当代码要求高性能的时候, 我们很可能需要引入变量去快速的修改对象中的数据.

## 在编程纪律中保持不变性

但declarative就此被抛弃了吗? 并不是, 看上去我们在代码层面上放弃了不变性, 但实际上, 我们只是把不变性放到了编程纪律之中. 当语言提供了锤子, 我们要靠纪律来保证不要砸到手指.

### 不变式 -- 保证迭代循环的正确性

Dijkstra很早就提出过不变式(invariant assertion)的概念. 在算法书中, 这个概念被一次次提及. 算法中的不变式可以理解为: 在算法执行过程中始终保持成立的 “规则” 或 “条件”. 它就像一个贯穿始终的 “隐形约束”, 帮助我们写出正确的算法。

譬如插入排序中的不变式为“第 i 次迭代前，数组的前 i 个元素已经有序”

```python
def insertion_sort(arr):
    # 循环不变式：每次迭代开始前，arr[0:i] 已经有序
    for i in range(1, len(arr)):
        key = arr[i]  # 当前待插入的元素
        j = i - 1     # 已排序部分的最后一个元素索引
        
        # 将比 key 大的元素后移
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]  # 元素后移
            j -= 1
        
        # 插入 key 到正确位置
        arr[j + 1] = key
        
        # 此时，arr[0:i+1] 已经有序（不变式成立）
    
    return arr  # 返回排序好的数组

# 使用示例
arr = [5, 2, 4, 6, 1, 3]
sorted_arr = insertion_sort(arr)
print(sorted_arr)  # 输出: [1, 2, 3, 4, 5, 6]
```

而二分查找的不变式为“每次迭代时，目标值若存在，必定在当前搜索区间 \[left, right] 内”

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1  # 初始化：搜索整个数组
    
    while left <= right:  # 只要区间存在，就继续查找
        mid = (left + right) // 2  # 取中间索引
        
        if arr[mid] == target:
            return mid  # 找到目标，直接返回
        
        elif arr[mid] < target:
            left = mid + 1  # 目标在右半部分，缩小左边界
            
        else:  # arr[mid] > target
            right = mid - 1  # 目标在左半部分，缩小右边界
            
        # 此时，目标值若存在，必在新的区间[left, right]内（不变式成立）
    
    return -1  # 区间为空，说明目标不存在
```

基本上不变式只和循环有关. 循环中我们修改了变量的值, 但总体目标还是要保持不变式依旧满足.
在实现算法时, 找到一个优秀的不变式往往是正确实现算法的关键. 随着不断积累算法, 寻找不变式的技能也会相应的提高.

### 声明式的API设计

另外, 虽然在具体实现上, 我们放弃了不变性, 但是在API设计上,  我们仍旧可以设计一些声明式的API作为模块的入口. 比较以下两种设计.
在处理简单的问题时, 无状态的API要比有状态的API更加灵活.

```python
def traffic_light(state, action):
    if state == "red" and action == "timer_expired":
        return "green"
    elif state == "green" and action == "timer_expired":
        return "yellow"
    elif state == "yellow" and action == "timer_expired":
        return "red"
    else:
        return state  # invalid state transform

# example
current_state = "red"
print(current_state)  # output: red

current_state = traffic_light(current_state, "timer_expired")
print(current_state)  # output: green

current_state = traffic_light(current_state, "timer_expired")
print(current_state)  # output: yellow
```

```python
class TrafficLight:
    def __init__(self):
        self.state = "red"  # 初始状态
    
    def update(self, action):
        if self.state == "red" and action == "timer_expired":
            self.state = "green"
        elif self.state == "green" and action == "timer_expired":
            self.state = "yellow"
        elif self.state == "yellow" and action == "timer_expired":
            self.state = "red"
        return self.state  # 返回新状态

# 使用示例
light = TrafficLight()
print(light.state)  # 输出: red

light.update("timer_expired")
print(light.state)  # 输出: green

light.update("timer_expired")
print(light.state)  # 输出: yellow
```
