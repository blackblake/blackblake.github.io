---
title: lab3
categories:
  - mit6.s081
  - lab
---
### 环境
1. 启动`qemu`和`gdb`: `make CPUS=1 qemu-gdb`，当前的这个终端窗口我们暂且称呼其为窗口1
2. 打开另一个终端窗口2，还是在xv6-labs-2021目录下，执行`gdb kernel/kernel`
3. 在gdb中输入`tui enable`可以进入源代码展示窗口，可以用`先按下Ctrl+x，然后按下Ctrl+a`来退出
4. 如果您想完全退出GDB程序：在GDB提示符下输入 `quit` 或简写 `q
5. 还记得窗口1吗？`vmprint`函数会在这个窗口进行输出，因为这个窗口1显示的是**QEMU的控制台输出**
	 ![[Pasted image 20250317143335.png|500]]
	 我们来看一下这里的输出。第一行是最高一级page directory的地址，这就是存在SATP或者将会存在SATP中的地址。第二行可以看到最高一级page directory只有一条PTE序号为0，它包含了中间级page directory的物理地址。第三行可以看到中间级的page directory只有一条PTE序号为128，它指向了最低级page directory的物理地址。第四行可以看到最低级的page directory包含了PTE指向物理地址。你们可以看到最低一级 page directory中PTE的物理地址就是0x10000000，对应了UART0（因为到此为止程序只执行了一条kvmmap语句`kvmmap(UART0, UART0, PGSIZE, PTE_R | PTE_W);`）

### 用户进程的内存分布
---
```c
// User memory layout.
// Address zero first:
//   text
//   original data and bss
//   fixed-size stack
//   expandable heap
//   ...
//   USYSCALL (shared with kernel)
//   TRAPFRAME (p->trapframe, used by the trampoline)
//   TRAMPOLINE (the same page as in the kernel)
```

`memlayou.h`中的这段代码注释描述了用户程序在内存中的布局结构。在大多数操作系统中，每个进程都有自己的独立虚拟地址空间，这段注释解释了这个地址空间是如何组织的。从低地址到高地址依次是：

1. **text（代码段）**: 存放程序的可执行代码。这是程序中的指令部分。
    
2. **original data and bss（数据段和未初始化数据段）**:
    
    - data: 存放已初始化的全局变量和静态变量
    - bss: 存放未初始化的全局变量和静态变量（系统会将它们初始化为0）
3. **fixed-size stack（固定大小的栈）**: 用于函数调用，存放局部变量、函数参数、返回地址等。栈通常从高地址向低地址增长。
    
4. **expandable heap（可扩展的堆）**: 用于动态内存分配（如malloc/free调用），可以根据需要扩展。堆通常从低地址向高地址增长。
    
5. **USYSCALL**: 这是一个与内核共享的区域，可能用于进程与内核之间的快速系统调用通信，减少上下文切换开销。
    
6. **TRAPFRAME**: 这个区域存储进程的陷阱帧（trapframe），当发生系统调用、中断或异常时，用来保存进程的状态（寄存器值等）。注释中提到它通过`p->trapframe`访问，这表明它是进程结构体中的一个字段。
    
7. **TRAMPOLINE**: 这是一个与内核共享同一页面的区域，用于实现用户空间和内核空间之间的安全切换。它包含从用户模式切换到内核模式的代码。

### `mappage()`
---
`mappages()` 函数可以将虚拟地址范围 `[va, va + size)` 映射到物理地址范围 `[pa, pa + size)`，并设置相应的访问权限。

`mappages()` 函数有五个参数，分别为

- `pagetable_t pagetable`：表示页表的指针，用于指定将要修改的页表。
- `uint64 va`：虚拟地址的起始地址。
- `uint64 size`：需要映射的虚拟地址范围的大小。
- `uint64 pa`：物理地址的起始地址。
- `int perm`：权限标志，用于设置 PTE 的权限。
