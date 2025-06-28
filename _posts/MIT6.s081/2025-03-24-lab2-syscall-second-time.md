---
title: lab2 syscall (second time)
date: 2025-03-24 03:39:16 +0800
categories:
- MIT 6.S081
- 实验
tags:
- dl
math: true
---

一、创建系统调用的流程
---
---
[来自miigon's blog](https://blog.miigon.net/posts/s081-lab2-system-calls/#如何创建新系统调用)

### step1 实现系统调用sys_name
首先在内核中合适的位置（取决于要实现的功能属于什么模块），实现我们的内核调用（在这里是 trace 调用）

>在`sys_name`函数中实现名为name的系统调用

比如我们的系统调用A会对进程进行操作，所以把A的实现sys_A函数放在 sysproc.c 较为合适。

### step2 添加序号
在 syscall.h 中加入新 system call 的序号：
```c
// kernel/syscall.h
// System call numbers
...
#define SYS_mkdir  20
#define SYS_close  21
#define SYS_trace  22 // here!!!!!
```
### step3 `sys_name`  函数的全局extern声明
用 extern 全局声明新的内核调用函数，并且在 syscalls 映射表中，加入从前面定义的编号到系统调用函数指针的映射

```c
// kernel/syscall.c
...
extern uint64 sys_write(void);
extern uint64 sys_uptime(void);
extern uint64 sys_trace(void);   // HERE
```
### step4 向`syscalls`数组中添加元素
```c
static uint64 (*syscalls[])(void) = {
...
[SYS_mkdir]   sys_mkdir,
[SYS_close]   sys_close,
[SYS_trace]   sys_trace,  // AND HERE
};
```
这里 [SYS_trace] sys_trace 是 C 语言数组的一个语法，表示以方括号内的值作为元素下标。比如 `int arr[] = {[3] 2333, [6] 6666}` 代表 arr 的下标 3 的元素为 2333，下标 6 的元素为 6666，其他元素填充 0 的数组。

### step5 在`usys.pl`脚本中添加条目
```c
# user/usys.pl
...
entry("sleep");
entry("uptime");
entry("trace");  # HERE
```

这个perl脚本在运行后会生成 `usys.S` 汇编文件，里面定义了每个 system call 的 **用户态跳板函数** ：

```plaintext
trace:		# 定义用户态跳板函数
li a7, SYS_trace	# 将系统调用 id 存入 a7 寄存器
ecall				# ecall，调用 system call ，跳到内核态的统一系统调用处理函数 syscall()  (syscall.c)
ret
```

### step6 ` user.h`
在用户态的头文件加入定义，使得用户态程序可以找到这个跳板入口函数。
```c
// user/user.h
// system calls
...
int sleep(int);
int uptime(void);
int trace(int);		// HERE
```

二、系统调用的流程
---
---

>1. user/user.h:		用户态程序调用跳板函数 trace()
>2. user/usys.S:		跳板函数 trace() 使用 CPU 提供的 ecall 指令，调用到内核态
>3. kernel/syscall.c	到达内核态统一系统调用处理函数 syscall()，所有系统调用都会跳到这里来处理。
>4. kernel/syscall.c	syscall() 根据跳板传进来的系统调用编号，查询 syscalls[] 表，找到对应的内核函数并调用。
>5. kernel/sysproc.c	到达 sys_trace() 函数，执行具体内核操作


三、锁
---
---

### 1）锁的代码

```c
// Acquire the lock.
// Loops (spins) until the lock is acquired.
void
acquire(struct spinlock *lk)
{
  push_off(); // disable interrupts to avoid deadlock.
  if(holding(lk))
    panic("acquire");

  // On RISC-V, sync_lock_test_and_set turns into an atomic swap:
  //   a5 = 1
  //   s1 = &lk->locked
  //   amoswap.w.aq a5, a5, (s1)
  while(__sync_lock_test_and_set(&lk->locked, 1) != 0)
    ;

  // Tell the C compiler and the processor to not move loads or stores
  // past this point, to ensure that the critical section's memory
  // references happen strictly after the lock is acquired.
  // On RISC-V, this emits a fence instruction.
  __sync_synchronize();

  // Record info about lock acquisition for holding() and debugging.
  lk->cpu = mycpu();
}
```
这是一个自旋锁(spinlock)的获取函数实现：

1. `push_off()`  禁用中断以避免死锁。这是因为如果在持有锁的过程中发生中断，可能导致系统死锁。

2. `if(holding(lk)) panic("acquire")`  检查当前CPU是否已经持有该锁，如果是则触发panic，防止重复获取同一个锁而导致死锁。
   >"panic"是一个重要的错误处理机制，表示系统遇到了无法恢复的严重错误
3. `__sync_lock_test_and_set(&lk->locked, 1)` 
  - 这是一个原子操作，尝试将锁的状态设置为1(表示锁定)，同时返回锁之前的状态：
  - 注释中解释了在RISC-V架构上，这个操作会转换为原子交换指令`amoswap.w.aq`
  - 如果返回0，表示锁之前是未锁定状态，现在已经成功获取
  - 如果返回非0，表示锁已经被其他CPU持有，需要继续尝试(自旋)

>4. `while(...) ;` 这是自旋锁的核心：如果锁已被占用，函数会在这个循环中"自旋"(不断尝试)直到成功获取锁。

5. `__sync_synchronize()`  内存屏障，确保锁获取之后的所有内存操作严格在获取锁之后执行，防止编译器和处理器的指令重排。

6. `lk->cpu = mycpu()`  记录哪个CPU获取了锁，用于调试和`holding()`函数检查。

>函数 release（1502）则做了与 acquire 相反的事：清除调试信息并释放锁。


四、sysinfo系统调用的实现
---
---

这个系统调用要实现两个功能：统计空闲内存的数量、统计进程数量

### （一）统计空闲内存——`count_free_mem`函数的实现

这个功能是关于内存的，所以此函数的实现代码放在`kalloc.c`当中，我们先来看这个文件中的代码：

#### 1）`freerange()`

```c
void
freerange(void *pa_start, void *pa_end)
{
  char *p;
  p = (char*)PGROUNDUP((uint64)pa_start);  //将 pa_start 转换为uint64类型后对齐，再转回char*型指针，表示当前要释放的页面地址
  
  for(; p + PGSIZE <= (char*)pa_end; p += PGSIZE)
    kfree(p);
}
```

1. `PGROUNDUP(addr)`：将地址 addr 向上对齐到页面边界（假设页面大小为 PGSIZE）
   - 物理内存以页面为单位管理，因此必须按 PGSIZE 对齐

2. `for`循环：每次移动一个页面大小的距离，并调用 `kfree(p)` 释放当前页面。

#### 2）`kfree(p)`——释放一个Page

```c
void
kfree(void *pa)
{
  struct run *r;

  // 检查传入的物理地址 `pa` 是否合法：
  // 1. 必须按页大小对齐（`PGSIZE` 的整数倍）
  // 2. 必须在内核的合法物理内存范围内（`end` 到 `PHYSTOP` 之间）
  if(((uint64)pa % PGSIZE) != 0 || (char*)pa < end || (uint64)pa >= PHYSTOP)
    panic("kfree"); // 否则触发内核崩溃

  // 安全措施：将释放的内存填充为垃圾值（这里用 `1`）
  // 如果后续有代码误访问已释放的内存，可能读到无效数据（0x010101...），便于调试
  memset(pa, 1, PGSIZE);

  // 将物理地址 `pa` 转换为空闲链表节点 `struct run*`
  // `struct run` 是空闲内存块的数据结构，通常只包含一个 `next` 指针
  r = (struct run*)pa;

  // 获取内存管理器的锁（`kmem.lock`），防止并发修改空闲链表
  acquire(&kmem.lock);

  // 将当前页面插入空闲链表头部：
  // 1. 让当前页面的 `next` 指向原空闲链表头
  // 2. 更新空闲链表头为当前页面
  r->next = kmem.freelist;
  kmem.freelist = r;

  // 释放锁
  release(&kmem.lock);
}
```
注意这里首次出现了`kmem.freelist`这个变量，它的含义是用于管理 物理内存页（Page） 的 空闲链表。

#### 3）`kalloc`——分配一个Page
```c
void *
kalloc(void)
{
    struct run *r;  // 定义一个临时指针，用于操作空闲链表节点

    // 获取内存管理器的锁（防止多线程竞争）
    acquire(&kmem.lock);

    // 从空闲链表头部获取一个空闲页
    r = kmem.freelist;

    // 如果链表非空（r != NULL），更新链表头指针
    if (r)
        kmem.freelist = r->next;  // 将链表头指向下一个节点

    // 释放锁（允许其他线程操作空闲链表）
    release(&kmem.lock);

    // 如果成功分配到页面（r != NULL），填充垃圾值（用于调试）
    if (r)
        memset((char*)r, 5, PGSIZE);  // 用 0x05 填充整个页面（检测悬垂指针）

    // 返回分配到的物理页地址（若失败则返回 NULL）
    return (void*)r;
}
```
这个函数的代码又为我们提供了freelist的基本操作方式，所以我们就可以模仿写出我们的`count_free_mem`函数：

#### 4）`count_free_mem`函数
```c
uint64
count_free_mem(void) // added for counting free memory in bytes (lab2)
{
  acquire(&kmem.lock); // 必须先锁内存管理结构，防止竞态条件出现
  
  // 统计空闲页数，乘上页大小 PGSIZE 就是空闲的内存字节数
  uint64 mem_bytes = 0;
  struct run *r = kmem.freelist;
  while(r){
    mem_bytes += PGSIZE;
    r = r->next;
  }

  release(&kmem.lock);

  return mem_bytes;
}
```

### （二）统计进程数量——`count_process`函数的 实现

我们在`proc.c`中看到了这样的一个函数：

```c
// 打印当前所有进程的状态信息（调试用）
void
procdump(void)
{
    // 进程状态字符串映射表（索引对应进程状态常量）
    static char *states[] = {
        [UNUSED]    "unused",  // 未使用
        [SLEEPING]  "sleep ",  // 睡眠中
        [RUNNABLE]  "runble",  // 可运行
        [RUNNING]   "run   ",  // 运行中
        [ZOMBIE]    "zombie"   // 僵尸状态
    };

    struct proc *p;    // 当前遍历的进程指针
    char *state;       // 进程状态字符串  

    // 遍历进程表（从 `proc[0]` 到 `proc[NPROC-1]`）
    for (p = proc; p < &proc[NPROC]; p++) {
        // 跳过未使用的进程槽位
        if (p->state == UNUSED)
            continue;

        // 获取进程状态字符串：
        // 1. 如果状态合法（在 上面定义的 states 数组范围内），取对应的字符串
        // 2. 否则显示 "???"（未知状态）
        if (p->state >= 0 && p->state < NELEM(states) && states[p->state])
            state = states[p->state];
        else
            state = "???";

        // 打印进程信息：PID + 状态 + 进程名
        printf("%d %s %s", p->pid, state, p->name);
        printf("\n");  // 换行
    }
}
```

1. `UNUSED、SLEEPING`等进程状态能够作为数组下标，是因为它们被定义为枚举常量或宏定义的整数值，本质上是整数


2. `p->state`是存储进程信息的结构体`struct proc`中的成员：
```c
enum procstate state;        // Process state
```

3. `for (p = proc; p < &proc[NPROC]; p++)` 这个好像存储了所有进程的数组是怎么来的？


答：在`proc.h`中有如下声明：`struct proc proc[NPROC];`，其中：
- NPROC 是系统允许的最大进程数；
- 每个元素 struct proc 是一个 进程控制块（PCB），保存进程的所有元数据；

### （三）整合实现`sys_info`

这里和trace系统调用的实现步骤相同，惟一需要注意的是`copyout`函数的使用：

```c
copyout(p->pagetable, addr, (char *)&st, sizeof(st))  //a example of copyout
```

sys_info的具体实现很简单，调用count_free_mem\()和count_process\()这两个函数即可

贴一张完成的照片，感觉lab2做的比lab1要轻车熟路一些

![description](/assets/Image/syscalllab.png){: w="300", h"200" }