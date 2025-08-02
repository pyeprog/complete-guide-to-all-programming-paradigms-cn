# Concurrent OOP

![[Think 2025-06-24 10.34.00.excalidraw]]
实际上OOP中的并发操作也大量的使用到了lock和condition variable. 使用上和共享内存模型一脉相承.

## Concurrent OOP的新特性

但concurrent OOP也有特殊的, 适用于对象系统的并发支持, 这个概念叫做monitor.
monitor是一个类, 它的对象内置了一个锁和至少一个condition variable. 它提供互斥访问的机制, 也提供 让访问对象的线程休眠或被唤醒的机制.

```java
public class MonitorExample {
    private final Object monitor = new Object();
    private boolean ready = false;
 
    public void awaitCondition() throws InterruptedException {
        synchronized (monitor) {
            while (!ready) {
                monitor.wait();
            }
        }
    }

    public void signalCondition() {
        synchronized (monitor) {
            ready = true;
            monitor.notify();
        }
    }

    public void synchronizedAccess() {
        synchronized (monitor) {
            // synchronized access code here
            System.out.println("Accessing shared resource safely.");
        }
    }
}
```

这里以java为例. java中提供了synchronized关键词, 配合monitor使用达到lock/unlock的目的. 在临界区中, 我们还可以使用monitor.wait()和monitor.notify()方法对线程进行休眠和唤醒.

因为在java中每个object都内置有锁和condition variable, 都可以被当做monitor使用. 所以当前实例this对象也可以.

```java
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
            // synchronized access code here
            System.out.println("Accessing shared resource safely.");
        }
    }
}
```

甚至

```java
public class MonitorExample {
    private boolean ready = false;
 
    public synchronized void awaitCondition() throws InterruptedException {
  while (!ready) {
   wait();
  }
    }

    public synchronized void signalCondition() {
  ready = true;
  this.notify();
    }

    public synchronized void synchronizedAccess() {
  // synchronized access code here
  System.out.println("Accessing shared resource safely.");
    }
}
```

monitor比起lock和condition variable, 提供了更简单, 更适合对象使用的api. 但缺点也很明显, 其控制粒度比较粗, 在性能敏感的场景不能满足需求.

基于这些特性, 当我们只需要简单粗粒度的互斥访问对象时, 可以采用monitor.

## Monitor的实践

monitor的实践, 主要注意写法上不要出错.

- 修改对象状态的所有方法都需要synchronized, 但读状态的方法同样需要synchronized.
- 但synchronized的方法中调用了其他类的方法需要万分小心, 因为如果它们也是synchronized方法, 则有可能导致死锁. (alien method problem)
