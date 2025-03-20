---
title: "lab2 syscall"
date: 2025-03-20 03:39:16 +0800
categories: [MIT6.S081, Lab]
tags: [os]     # TAG names should always be lowercase
---
## Lab2A trace

实现一个叫trace的系统调用，在user/trace.c中有使用trace的源码，而我们的目的就是让这一段用户代码能够跑通，输出我们希望打印的系统调用函数的结果。

trace接受一个整数参数trace_mask，通过二进制位的标记来输出系统调用的结果。例如trace 32，表示输出read函数的调用结果
### step1
---
在`kernel/sysproc.c`中实现sys_trace系统调用

```c
uint64 sys_trace(void) {
   int trace_mask;
   
   // 从用户空间获取系统调用的第一个参数（跟踪掩码）
   // 参数索引为0表示第一个参数
   argint(0, &trace_mask);
   
   // 检查掩码是否有效
   if (trace_mask < 0)
       return -1;
   
   // 获取当前进程的进程控制块指针
   struct proc *p = myproc();
   
   // 设置当前进程的跟踪掩码
   // 这个掩码是一个位图，每一位对应一个系统调用号
   // 如果某位为1，则对应的系统调用会被跟踪
   p->trace_mask = trace_mask;

   return 0;
}
```

### step2
---
在`kernel/proc.c`中修改`fork()`函数，将父进程的track_mask传给子进程。
```c
//add a line of code:
np->trace_mask = p->trace_mask;
```

### step3
---
修改`syscall()`——这是实际执行跟踪的地方。所有系统调用都会经过 `syscall()` 函数，它是系统调用的中央处理点。只有在调用syscall()时才知道到底要不要输出调用信息，以及输出调用结果：

```c
void
syscall(void)
{
  int num;                     // 系统调用号
  struct proc *p = myproc();   //用myproc()函数获取当前执行进程的进程控制块PCB
  
  // 从trapframe中获取系统调用号，在RISC-V架构中，系统调用号存储在a7寄存器中
  // trapframe和proc这两个结构体都定义在proc.h
  num = p->trapframe->a7;
  
  // 验证系统调用号的有效性，并且确保对应的处理函数存在
  if(num > 0 && num < NELEM(syscalls) && syscalls[num]) {
    
    // 调用对应的系统调用处理函数并将返回值存储在a0寄存器中（RISC-V的返回值寄存器）
    p->trapframe->a0 = syscalls[num]();
    
    /* 跟踪功能：检查当前系统调用是否需要被跟踪（通过位掩码检查）
     1 << num 创建一个只有第num位为1的位掩码
     如果进程的trace_mask中对应位也为1，则说明需要跟踪此系统调用*/
    if ((1 << num) & p->trace_mask)
        // 打印跟踪信息：进程ID、系统调用名称和返回值
        printf("%d: syscall %s -> %d\n", p->pid, syscall_name[num - 1], p->trapframe->a0);
  } else {
	    // 处理无效的系统调用号：打印错误信息
	    printf("%d %s: unknown sys call %d\n",p->pid, p->name, num);
	    p->trapframe->a0 = -1;// 设置返回值为-1，表示调用失败
	}
}
```

### 三个步骤之间的联系
---
这三个步骤形成了完整的工作流程：

1. 第一步设置跟踪参数（配置阶段）
2. 第二步确保跟踪设置在进程创建时能够被继承（传播阶段）
3. 第三步在实际系统调用发生时执行跟踪（执行阶段）

这种设计遵循了操作系统内核中常见的模式：**配置 -> 传播 -> 执行**。没有任何一个步骤，整个功能都无法正常工作，它们共同构成了一个完整的系统调用跟踪机制。

## Lab2B Sysinfo

在本作业中，您将添加一个系统调用sysinfo，它收集有关正在运行的系统的信息。这个系统调用有一个参数：一个指向结构体sysinfo的指针（参见kernel/sysinfo.h）。内核应该填充这个结构体的字段：freemem字段应该设置为空闲内存的字节数，nproc字段应该设置为状态不是UNUSED的进程数。

### step1
---
在`kernel/kalloc.c`中添加统计可用的内存字节数的函数`nfreemem()`：

```c
/**
 * nfreemem - 计算系统中可用的空闲内存总量（以字节为单位）
 *
 * 该函数遍历空闲内存链表，计算可用的物理内存页数，
 * 然后将页数转换为字节数返回
 *
 * 返回值: 系统中可用的空闲内存总量（字节）
 */
uint64 nfreemem() {
    uint64 cnt = 0;        // 初始化计数器，用于记录空闲内存页数
    struct run *r;         // 定义指向空闲内存块的指针
    
    acquire(&kmem.lock);   // 获取内存管理锁，防止并发访问导致的竞争条件
    
    r = kmem.freelist;     // 获取空闲内存链表的头部
    
    // 遍历整个空闲内存链表
    while (r) {
        cnt++;             // 增加空闲页计数
        r = r->next;       // 移动到下一个空闲内存块
    }
    
    release(&kmem.lock);   // 释放内存管理锁
    
    return cnt * PGSIZE;   // 返回空闲内存总字节数（页数 × 每页大小）
}
```

### step2
---
在`kernel/proc.c`中添加统计进程状态不为UNUSED的进程数函数`nproc()`：

```c
uint64
nproc(void)
{
    uint64 cnt = 0;
    struct proc *p;
	
	#`proc`是一个数组，存储了系统中所有进程PCB；
	#`NPROC`是一个常量，定义了系统中最大可同时存在的进程数量。即`proc`数组的大小；
	#所以这个for循环实际上是遍历当前所有正在运行的进程
    for (p = proc; p < &proc[NPROC]; p++)
    {
        acquire(&p->lock);
        if (p->state != UNUSED)
            cnt++;
        release(&p->lock);
    }
    return cnt;
}
```

### step3
---
在`kernel/sysproc.c`中添加系统调用入口: `sys_sysinfo()`函数是`sysinfo`系统调用的实现。

```c
/**
 * sys_sysinfo - 实现 sysinfo 系统调用，返回系统信息
 *
 * 该函数填充 sysinfo 结构体，包含系统空闲内存、进程数等信息，
 * 然后将这些信息拷贝到用户空间提供的地址处。
 *
 * 系统调用参数:
 *   - 用户空间中 struct sysinfo 的地址
 * 
 * 返回值:
 *   - 成功返回0
 *   - 失败返回-1（例如，无法复制到用户空间）
 */
uint64
sys_sysinfo(void)
{
    uint64 addr;               // 用户提供的 sysinfo 结构体地址
    struct sysinfo info;       // 内核空间中的 sysinfo 结构体
    struct proc *p = myproc(); // 获取当前进程的进程控制块
    
    // 从用户空间获取第一个参数（sysinfo结构体的地址）
    argaddr(0, &addr);
    
    // 填充 sysinfo 结构体（用到step1,step2实现的两个函数）
    info.freemem = nfreemem(); // 获取系统空闲内存大小
    info.nproc = nproc();      // 获取系统中进程数量
    
    // 将填充好的 sysinfo 结构体复制回用户空间
    // copyout 函数将内核空间的数据拷贝到用户空间
    // 参数: 页表、目标地址、源地址、大小
    if (copyout(p->pagetable, addr, (char *)&info, sizeof(info)) < 0)
        return -1;             // 拷贝失败，返回错误
        
    return 0;                  // 成功执行，返回0
}
```


## 补充知识
---
1. **xv6 kernel source files**![[截屏2025-03-14 15.08.48.png|500]]
2. `kernrl/sysproc.c`这个文件中是与进程相关的系统调用的**实现**，如`sys_exit()`,`sys_trace` and `sys_fork()`...

3. `kernel/sysproc.c`中的sys_trace函数和trace系统调用有什么区别
	- 当用户程序通过系统调用接口调用`trace`时，内核会调用`sys_trace`函数来实际处理这个系统调用；
	- `sys_trace`是`trace`系统调用在内核中的实现；
	- `sys_trace`包含了实际的跟踪功能实现，而`trace`只是一个向内核传递参数的包装接口；

4. `kernel/proc.c` 文件:  主要负责进程管理相关的功能实现，包括：
	-  **进程数据结构定义**：它包含了进程控制块 (PCB) 的实现细节和进程表的管理；
	-  **进程创建与销毁**：实现了 `fork()`、`exit()` 等关键系统调用的核心逻辑；
	-  **进程调度**：包含进程调度器的实现，如 `scheduler()` 函数；
	-  **进程状态转换**：管理进程在运行、就绪等状态之间的转换；
	-  **进程内存管理**：如分配和释放进程的地址空间；

5. `sysinfo`系统调用的`sys_sysinfo`实现函数中，为什么需要用`copyout`函数将内核空间的数据拷贝到用户空间？
	这是因为xv6采用了内核和用户进程分离的页表机制，详见Lec4笔记

