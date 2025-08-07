# 基于OOP的并发模型

OOP中的并发操作也大量的使用到了`lock`和`condition variable`, 使用上和共享内存模型一脉相承.

## OOP并发模型的新特性

并发OOP中也存在特殊概念，适用于对象系统的并发操作, 这个概念叫做**monitor**。

Monitor是一种类，其对象内部内置一个lock和至少一个condition variable。它不仅提供互斥访问的机制，还支持让访问该对象的线程休眠或被唤醒的功能，从而有效管理并发环境下的同步与通信。换句话说, monitor把lock和condition variable整合到了同一个对象中, 并使其更方便使用. 

::::{tab-set}

:::{tab-item} object作为monitor

这里以java为例. 

java中提供了synchronized关键词, 配合monitor使用达到lock/unlock的目的. 在临界区中, 我们还可以使用monitor.wait()和monitor.notify()方法对线程进行休眠和唤醒.

```{code} java
:linenos:
:filename: objectAsMonitor.java
:emphasize-lines: 2,6,8,14,16,21
:caption: 创造一个独立的object对象作为monitor使用.

public class MonitorExample {
    // 构造一个object对象作为monitor
    private final Object monitor = new Object();
    private boolean ready = false;

    public void awaitCondition() throws InterruptedException {
        // 使用synchronized关键词, 使得这一段代码只能被互斥访问.
        synchronized (monitor) {
            while (!ready) {
                // monitor作为condition variable使用
                monitor.wait();
            }
        }
    }

    public void signalCondition() {
        synchronized (monitor) {
            ready = true;
            // monitor作为condition variable使用
            monitor.notify();
        }
    }

    public void synchronizedAccess() {
        synchronized (monitor) {
            System.out.println("Accessing shared resource safely.");
        }
    }
}
```

:::

:::{tab-item} 显式使用this作为monitor

因为在java中每个object都内置有锁和condition variable, 都可以被当做monitor使用. 所以当前实例this对象也可以.

```{code} java
:linenos:
:filename: thisAsMonitor.java
:emphasize-lines: 5,7,13,15,19
:caption: 直接使用this对象作为monitor使用

public class MonitorExample {
    private boolean ready = false;

    public void awaitCondition() throws InterruptedException {
        synchronized (this) {
            while (!ready) {
                this.wait();
            }
        }
    }

    public void signalCondition() {
        synchronized (this) {
            ready = true;
            this.notify();
        }
    }

    public void synchronizedAccess() {
        synchronized (this) {
            System.out.println("Accessing shared resource safely.");
        }
    }
}
```
:::

:::{tab-item} 隐式使用this作为monitor
```{code} java
:linenos:
:filename: defaultThisAsMonitor.java
:emphasize-lines: 4,6,10,12
:caption: `隐式`使用this对象作为monitor, 此时`synchronized`关键词放在方法定义前.

我们甚至可以这样写, 把synchronized关键词提到方法定义前, 表明整个方法都是互斥的. `this.wait()`和`this.notify()`可以省略`this.`, 直接在临界区调用`wait()`和`notify()`.

public class MonitorExample {
    private boolean ready = false;

    public synchronized void awaitCondition() throws InterruptedException {
        while (!ready) {
            wait();  // 甚至可以省略this关键词
        }
    }

    public synchronized void signalCondition() {
        ready = true;
        notify();  // 甚至可以省略this关键词
    }

    public synchronized void synchronizedAccess() {
        System.out.println("Accessing shared resource safely.");
    }
}
```
:::
::::

monitor比起lock和condition variable, 提供了更简单, 更适合对象使用的api. 

但缺点也很明显, 它为了使用方便, 牺牲了灵活性, 它的控制粒度比较粗, 在性能敏感的场景可能达不到性能要求.

基于这些特性, `当我们只需要简单粗粒度的互斥访问对象时, 可以采用monitor`.

## Monitor的实践

monitor的实践, 主要注意写法上不要出错.

::::{tab-set}

:::{tab-item} 遗漏synchronize

```{code} java
:linenos:
:filename: dirtyRead.java
:emphasize-lines: 17
:caption: 对临界区数据的所有读写操作都应该是synchronized

public class DirtyRead {
    private int data = 0;

    // 写方法置为synchronized
    public synchronized void write(int value) {
        System.out.println("Writing value: " + value);
        try {
            Thread.sleep(100); // Simulate delay during write
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        data = value;
        System.out.println("Value written: " + value);
    }

    // 忘记把读方法置为synchronized, 这会导致读到脏数据
    public int read() {
        System.out.println("Reading value: " + data);
        return data;
    }
}
```

:::

:::{tab-item} Alien method
```{code} java
:linenos:
:filename: alienMethod.java
:emphasize-lines: 4,13-15
:caption: 在临界区内调用其他库方法要小心{abbr}`这种问题(alien method problem)`

class A {
    public synchronized void foo(B b) {
        System.out.println("A.foo(): Holding A's lock, calling B.bar()");
        b.bar(this);  // 在用this锁定的临界区内, 调用了bar方法, 但bar中偷偷用this加锁, 导致死锁
        System.out.println("A.foo(): Finished calling B.bar()");
    }
}

// 假设B定义在某个三方库中, 你并不了解, 它(不恰当)的使用了传入的对象a作为monitor
class B {
    public void bar(A a) {
        System.out.println("B.bar(): Holding B's lock, trying to synchronize on A");
        synchronized (a) {
            System.out.println("B.bar(): Acquired lock on A");
        }
        System.out.println("B.bar(): Finished");
    }
}
```
:::

::::
