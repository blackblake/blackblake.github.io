---
title: "lab3 pgtbl"
date: 2025-03-26 03:39:16 +0800
categories: [MIT6.S081, os_Lab]
tags: [os]     # TAG names should always be lowercase
---

[本篇笔记参考了tzyt's blog](https://ttzytt.com/2022/07/xv6_lab3_record/index.html#post-comment)

Speedup system call
---
---

### 1）mappage

题目提示要用到`mappage`这个函数：
```c
// 为从虚拟地址va开始的连续虚拟地址创建页表项(PTEs)，这些虚拟地址映射到从物理地址pa开始的物理地址。
// 成功则返回0，如果walk()无法分配所需的页表页则返回-1
int
mappages(pagetable_t pagetable, uint64 va, uint64 size, uint64 pa, int perm)
{
  // pagetable: 页表根目录指针
  // va: 要映射的起始虚拟地址
  // size: 要映射的区域大小(字节)
  // pa: 起始物理地址
  // perm: 页表项的权限标志位(如PTE_R、PTE_W等)
  
  uint64 a, last;  // a: 当前处理的页对齐虚拟地址，last: 最后一项的页对齐地址
  pte_t *pte;      // 指向页表项的指针

  if(size == 0)panic("mappages: size");    // 如果映射大小为0，这是不允许的
  
  // 将起始虚拟地址向下对齐到页面边界(清除低12位)
  a = PGROUNDDOWN(va);
  // 计算结束地址(va+size-1)并向下对齐到页面边界
  last = PGROUNDDOWN(va + size - 1);

  // 循环处理每一页
  for(;;){
    // 使用walk函数查找/创建虚拟地址a指向的页表项，1表示需要时创建新页表
    if((pte = walk(pagetable, a, 1)) == 0)
      return -1;  // walk失败返回-1
    
    // 若walk函数返回的页表项pte已被映射过了，则报错
    if(*pte & PTE_V)
      panic("mappages: remap");  
    
    // 设置页表项：将 作为参数被传入的目标物理地址pa 转换为页表项格式存入页表中，添加权限和有效位
    *pte = PA2PTE(pa) | perm | PTE_V;
    
    // 如果已经处理完所指定的最后的虚拟地址，退出循环
    if(a == last)
      break;
    
    // 若还有虚拟地址需要映射，则移动到下一页(虚拟地址增加4KB)
    a += PGSIZE;
    // 对应的物理地址也增加4KB
    pa += PGSIZE;
  }
  return 0;  // 所有映射成功完成
}
```

### 2）内存地址空间分布

`memlayout.h`中描述了虚拟地址空间的分布层次

![addralloc](/assets/Image/addralloc.png)

#### **1. QEMU 模拟的硬件设备内存映射**
这些地址由 QEMU 的 `virt` 机器模型定义（见 `hw/riscv/virt.c`），用于访问硬件寄存器：

| 地址范围       | 设备/功能                | 说明                                                                 |
|----------------|--------------------------|----------------------------------------------------------------------|
| `0x00001000`   | **Boot ROM**             | QEMU 提供的启动代码（机器模式启动时执行）                            |
| `0x02000000`   | **CLINT**（核心本地中断器）| 包含定时器（`MTIMECMP`）和时钟计数器（`MTIME`）                      |
| `0x0C000000`   | **PLIC**（平台级中断控制器）| 管理外部设备中断（如 UART、磁盘）                                    |
| `0x10000000`   | **UART0**                | 串口设备寄存器（用于控制台输入输出）                                 |
| `0x10001000`   | **VIRTIO0**              | 虚拟磁盘设备寄存器（用于文件系统）                                   |
| `0x80000000`   | **内核加载地址**          | QEMU 的 Boot ROM 跳转到这里（机器模式），内核代码和数据从此处开始    |

---

#### **2. 内核使用的物理内存布局**
从 `0x80000000` 开始的内存由内核管理：

| 地址范围            | 用途                                               |
|---------------------|--------------------------------------------------|
| `0x80000000`        | **内核入口**（`entry.S`），随后是内核代码段（`text`）和数据段（`data`） |
| `end`               | 内核代码结束位置，之后是 **动态分配的物理页Free memory**（供内核和用户进程使用） |
| `PHYSTOP`           | 内核可用的物理内存上限（`KERNBASE + 128MB`，具体取决于配置）          |

---

#### **3. 内核虚拟地址空间布局**
内核为每个进程维护 **用户空间** 和 **内核空间** 的虚拟内存映射：

##### **（1）内核高地址区域**
| 地址/宏定义          | 用途                                                      |
|----------------------|---------------------------------------------------------|
| `TRAMPOLINE`         | 蹦床页面（`MAXVA - PGSIZE`），存放用户-内核切换的汇编代码（如 `trampoline.S`） |
| `KSTACK(p)`          | 每个进程的内核栈（`p` 是进程 ID），周围有 **保护页Guard page** 防止溢出         |

##### **（2）用户空间布局（从低地址到高地址）**
| 地址/宏定义          | 用途                                                                 |
|----------------------|----------------------------------------------------------------------|
| `0x0`                | 用户程序代码（`text`）                                               |
| （向上增长）         | 初始数据（`data`）、未初始化数据（`bss`）                            |
| （向下增长）         | 用户栈（固定大小）                                                   |
| （向上增长）         | 堆（动态扩展）                                                       |
| `USYSCALL`（可选）   | 共享页面（如存储进程 ID，加速系统调用）                               |
| `TRAPFRAME`          | 陷阱帧（`trapframe`），保存用户进程陷入内核时的寄存器状态             |
| `TRAMPOLINE`         | 与内核共享的蹦床页面（用于安全切换权限级别）                          |

---

#### **4. 关键宏定义详解**
| 宏定义               | 说明                                                                 |
|----------------------|----------------------------------------------------------------------|
| `KERNBASE`           | 内核物理内存起始地址（`0x80000000`）                                 |
| `PHYSTOP`            | 内核可用物理内存的结束地址（`KERNBASE + 128MB`）                     |
| `MAXVA`              | 最大虚拟地址（RISC-V Sv39 为 `0x3FFFFFFFFF`）                        |

---


#### **总结**
- **低物理地址**（`0x0` ~ `0x80000000`）：预留给 QEMU 模拟的设备寄存器。
- **内核物理内存**（`0x80000000` ~ `PHYSTOP`）：存放内核代码和动态分配的内存。
- **用户虚拟空间**：从低到高依次是代码、堆栈、共享页、陷阱帧和蹦床页。
- **内核虚拟空间**：高地址包含蹦床页和每个进程的内核栈。


>ps: 这里我有一个疑问，既然trampoline也是与内核共享的页面，为什么不把要共享的pid值放在这里面，而要单开一个usyscall页面？
> 
> 答：
> - TRAMPOLINE 的职责： 
>   - 用于 安全切换执行权限（用户态↔内核态），存放与上下文切换相关的汇编代码（如保存/恢复寄存器、修改 satp 寄存器等）。它是纯代码页，不应混入数据。 
> - USYSCALL 的职责： 
>   - 专用于 加速只读系统调用（如 getpid），存放只读共享数据（如 pid）。它是纯数据页，与执行逻辑无关。 
> - 混用会导致： 
>   - 安全风险（如意外修改蹦床代码）。 
>     - 维护复杂性（需区分代码和数据访问权限）。


### 3）proc_pagetable

`proc_pagetable` 是操作系统内核中用于 ***在创建进程时，为进程创建其初始页表*** 的函数，主要完成以下任务：

1. 分配页表内存
   - 调用 kalloc() 申请一页物理内存，作为进程的 顶级页表（PGD）。
2. 映射内核空间
   - 将内核的代码、数据等固定地址（如 KERNBASE 以上）映射到页表中，确保所有进程共享内核内存（例如系统调用时能访问内核代码）。
3. 映射用户空间关键区域
   - 蹦床页面（TRAMPOLINE）：映射到虚拟地址最高端（如 MAXVA - PGSIZE），用于安全切换用户态/内核态。
   - 陷阱帧（TRAPFRAME）：保存用户进程陷入内核时的寄存器状态。
   - USYSCALL（可选）：共享只读数据（如 pid），加速系统调用（如 getpid）。
4. 返回页表指针
   - 若成功，返回初始化好的页表指针；失败时释放内存并返回 0。

下面来看具体代码

我们发现这个函数里有使用 `mappages()` 来创建 `trampoline` 和 `trapframe` 页面的代码，由于usyscall和这两个一样都是页面，所以可以参考一下：

```c
// map the trampoline
if(mappages(pagetable, TRAMPOLINE, PGSIZE,
            (uint64)trampoline, PTE_R | PTE_X) < 0){
    uvmfree(pagetable, 0);
    return 0;
}

// map the trapframe just below TRAMPOLINE, for trampoline.S.
if(mappages(pagetable, TRAPFRAME, PGSIZE,
            (uint64)(p->trapframe), PTE_R | PTE_W) < 0){
    //如果映射失败
    uvmunmap(pagetable, TRAMPOLINE, 1, 0);
    uvmfree(pagetable, 0);
    return 0;
}
```

>这里有一个细节是：在第一段映射trampoline的时候，没有`unmap`这一行；
> 
>而第二段映射`trapframe`的时候就有了一行`unmap`，注意它的功能是取消之前给`trampoline`分配的映射，而不是取消给`trapframe`的映射（因为trapframe映射失败了，根本没得取消）
> 
> 以此类推，我们可以知道，在映射`usyscall`的代码中，必须在映射失败的错误处理代码中这样写：


```c
if(mappages(pagetable, USYSCALL, PGSIZE, (uint64)(p->usyscall), PTE_R | PTE_U) < 0){
    
    //如果映射usyscall失败
    uvmunmap(pagetable, TRAMPOLINE, 1, 0); //取消之前已经成功映射的trampoline
    uvmunmap(pagetable, TRAPFRAME, 1, 0);  //取消之前已经成功映射的trapframe
    uvmfree(pagetable, 0);
    return 0;
  }
```

### 4）proc_freepagetable

我们在用`proc_pagetable`创建进程时，多创建了一个给页面`usyscall`的映射，所以需要在销毁进程时也取消这个映射

### 5）allocproc

我们已经成功创建了从虚拟内存到物理的映射，但是并没有在创建进程的时候申请这个物理内存。如果不去申请这个物理内存，我们就会尝试把一个虚拟内存映射到空指针上，所以还需要改一下 allocproc() 这个函数

Print a page table
---
---
在这一节我们需要实现一个`vmprint()`函数用于打印页表，它接受一个`pagetable_t`类型的参数，我们先来看一下`pagetable_t`是什么

### 1）pagetable_t
在`riscv.h`中发现其定义：
```c
typedef uint64 *pagetable_t; // 512 PTEs
```

- 这说明它是指向页表的指针，而页表本身是一个由 uint64（64 位无符号整数）组成的数组
- 在xv6中，每个页表包含 2^9 = 512 个页表项（PTE），因此注释中注明 `// 512 PTEs`
- 所以我们的这个`vmprint`函数接受一个页表作为参数

### 2）`freewalk`

文档中提示我们可以参考这个函数：
```c
// 递归地释放页表中的页
// 此函数正常运行的前提——所有叶子结点都已被移除
void
freewalk(pagetable_t pagetable)
{
  // 遍历当前页表中的所有 512 个页表项 (PTE)
  for(int i = 0; i < 512; i++){
    pte_t pte = pagetable[i];  // 获取第 i 个页表项
    
    // 检查 PTE 是否有效（PTE_V）且不是叶子节点（非 R/W/X）
    if((pte & PTE_V) && (pte & (PTE_R|PTE_W|PTE_X)) == 0){
      // 这个 PTE 指向一个更低层级的页表（非叶子）
      uint64 child = PTE2PA(pte);     // 从 PTE 中提取子页表的物理地址
      freewalk((pagetable_t)child);   // 递归释放子页表
      pagetable[i] = 0;               // 清零当前 PTE
    } 
    
    // 如果 PTE 有效且是叶子节点（R/W/X 至少一个被设置）
    else if(pte & PTE_V){
      panic("freewalk: leaf"); // 叶子映射应已被移除（这是freewalk函数正常运行的前提），否则报错
    }
    
    // 如果 PTE 无效（PTE_V = 0），则直接跳过
  }
  
  // 释放当前页表占用的物理页
  kfree((void*)pagetable);
}
```
1. `pte_t`：一个宏，和`pagetable_t`一起被定义在`riscv.h`的末尾
2. `pagetable[i]`：
3. `PTE2PA(pte)`：通过 PTE2PA 宏将 PTE 转换为物理地址


### 3）叶子结点

解释一下`freewalk`函数中的“叶子结点”的概念：

在 多级页表结构（如 xv6 的三级页表）中：

1. 非叶子节点：
页表项（PTE）指向 下一级页表（例如顶级页表的 PTE 指向中间页表）。
   - 特征：PTE 的 PTE_V 位为 1，但 PTE_R/PTE_W/PTE_X（可读/可写/可执行）权限位均为 0。
   - 作用：仅用于索引下一级页表，不直接映射物理页。

2. 叶子节点：
页表项（PTE）直接指向 物理页帧（即最终的数据页或代码页）。
   - 特征：PTE 的 PTE_V 位为 1，且至少有一个权限位（PTE_R/PTE_W/PTE_X）为 1。
   - 作用：完成虚拟地址到物理地址的最终映射。

### 4）`vmprint()`实现

```c
void 
vmprint(pagetable_t pagetable, uint dep){
  if(dep == 0)
    printf("page table %p\n", pagetable);
  for(int i = 0; i < 512; i++){
    pte_t pte = pagetable[i];
    if(pte & PTE_V){
      for(int j = 0; j < dep; j++)
        printf(".. ");
      uint64 child = PTE2PA(pte);
      printf("..%d: pte %p pa %p\n", i, pte, child);
      if(dep < 2)
        // 如果层数等于 2 就不需要继续递归了，因为这是叶子节点
        vmprint((pagetable_t) child, dep + 1);
    }
  } 
}
```

Access
---
---
[第三个题目在这篇blog里讲的很清楚](https://ttzytt.com/2022/07/xv6_lab3_record/index.html#post-comment)

这里只提挈几个细节：

1. `pgaccess()`函数的三个参数怎么传入给内核态检测页表使用？
2. 最后得到的掩码值如何返回给`pgaccess()`函数？


3. `walk`函数：对于一个给定的页表和虚拟地址，walk() 函数会返回对应这个虚拟地址的叶子 **PTE**


4. 主循环：
```c
for(int i = 0; i < ck_siz; i++){
    if((fir_pte[i] & PTE_A) && (fir_pte[i] & PTE_V)){
        mask |= (1 << i);  //由第0位开始，每次向更高的一位写入
        fir_pte[i] ^= PTE_A; // 复位
    }
}
```
- `if((fir_pte[i] & PTE_A) && (fir_pte[i] & PTE_V))`
  - fir_pte[i] & PTE_A：检查当前 PTE 的 访问位（PTE_A） 是否被置 1（即该页是否被访问过）。
  - fir_pte[i] & PTE_V：检查当前 PTE 的 有效位（PTE_V） 是否被置 1（即该页是否有效）。
  - 只有 两个条件同时满足（页有效且被访问过），才会进入 if 块。

- mask |= (1 << i);
  - 1 << i：生成一个只有第 i 位为 1 的掩码（例如 i=2 → 0b100）。
  - mask |= ...：将 mask 的第 i 位置 1，表示第 i 个 PTE 满足条件（被访问过且有效）。
    - 作用：最终 mask 是一个位掩码，每一位 i 表示 fir_pte[i] 是否被访问过。
  - fir_pte[i] ^= PTE_A;


- PTE_A 是访问位（例如 0x40，即 1 << 6）。
  - ^=（异或赋值）：翻转 PTE_A 位。
  - 如果 PTE_A 原本是 1，异或后变为 0（复位访问位）。
  - 如果 PTE_A 原本是 0，异或后变为 1（但这里不会发生，因为前面已经检查 PTE_A 为 1）。
  - 作用：清除访问位，表示该页的访问状态已被处理。
