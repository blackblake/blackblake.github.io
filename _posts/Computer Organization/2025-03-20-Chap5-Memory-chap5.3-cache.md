---
title: chap5.3 cache
date: 2025-03-20 03:39:16 +0800
categories:
- 计算机组成原理
tags:
- dl
math: true
---

### Part I:  Appendix Knowledge
---
**1-1 Byte**
	**内存的最小可寻址单位是字节(byte)**，具体原因与硬件相关
	如B, MB, KB, GB都是以B(byte)为单位的

### Part II:  直接映射
---
##### 2-1: Index in cache

> **Index = (Mem addr) mod (Number of blocks in the cache)**
	
If the number of entries in the cache is a power of 2, then modulo can be
computed simply by using the **\[low-order $log_2$ (cache size in blocks) bits of the address]**. 
	
Thus, an 8-block cache uses the 3 lowest bits (8 = $2^3$) of the block address. 
	
For example, Figure 5.8 shows how the memory addresses between 1ten
(00001two) and 29ten (11101two) map to locations 1ten (001two) and 5ten (101two) in a
direct-mapped cache of eight words.

![Pasted image 20241120174448](/assets/Image/Pasted image 20241120174448.png){: w="500"}

##### 2-2  Index

![Pasted image 20241120175253](/assets/Image/Pasted image 20241120175253.png){: w="500"}

##### 2-3 Offset, Index, Tag

[![](https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Direct-Mapped_Cache_Snehal_Img.png/500px-Direct-Mapped_Cache_Snehal_Img.png)]

【block块数=block总容量(单位byte)÷单个block大小】
Consider a main memory of 16 kilobytes, which is organized as 4-byte blocks, and a direct-mapped cache of 256 bytes with a block size of 4 bytes. Because the main memory is 16kB, we need a minimum of 14 bits to uniquely represent a memory address.($log_2{16kB}=14$)

Since each cache block is of size 4 bytes, the total number of sets in the cache is 256/4, which equals 64 sets. (64 lines)

The **incoming address** to the cache is divided into bits for [Offset](https://en.wikipedia.org/wiki/CPU_cache#Cache_entry_structure "CPU cache"), [Index](https://en.wikipedia.org/wiki/CPU_cache#Cache_entry_structure "CPU cache") and [Tag](https://en.wikipedia.org/wiki/CPU_cache#Cache_entry_structure "CPU cache").

>- **_Offset_** corresponds to the bits used to determine the BYTE(or COLOMN,vividly) to be accessed from the cache line. Because the cache lines are 4 bytes long, there are _2 offset bits_.

>- **_Index_** corresponds to bits used to determine the SET(or LINE, vividly) of the Cache. There are 64 sets in the cache, and because 2^6 = 64, there are _6 index bits._

>- **_Tag_** corresponds to the remaining bits. This means there are 14 – (6+2) = _6 tag bits_, which are stored in tag field to match the address on cache request. (Maybe work by examine whether the Tag bits are the same as the tag field of the cache)


Below are memory addresses and an explanation of which cache line they map to:

1. Address `0x0000` (tag - `0b00_0000`, index – `0b00_0000`, offset – `0b00`) corresponds to block 0 of the memory and maps to the set 0 of the cache.
2. Address `0x0004` (tag - `0b00_0000`, index – `0b00_0001`, offset – `0b00`) corresponds to block 1 of the memory and maps to the set 1 of the cache.
3. Address `0x00FF` (tag – `0b00_0000`, index – `0b11_1111`, offset – `0b11`) corresponds to block 63 of the memory and maps to the set 63 of the cache.
4. Address `0x0100` (tag – `0b00_0001`, index – `0b00_0000`, offset – `0b00`) corresponds to block 64 of the memory and maps to the set 0 of the cache.
  `(what does the '1' in tag bits mean?)`

##### 2-4  Cache before and after Reference

Figure 5.7 shows a simple cache, before and after requesting a data item that is not initially in the cache. Before the request, the cache contains a collection of recent references $X_1, X_2, …, X_{n−1}$, and the processor requests a word $X_n$ that is **NOT IN THE CACHE**. This request results in a miss, and the word $X_n$ is brought from memory into the cache.

![Pasted image 20241120191138](/assets/Image/Pasted image 20241120191138.png){: w="600"}


### Part III:  Accessing a Cache
---
#### 3-1  valid bit
Below is a sequence of **nine memory references to an empty eight-block cache**, including the action for each reference. Figure 5.9 shows how the contents of the cache change on each miss.
![Pasted image 20241120191546](/assets/Image/Pasted image 20241120191546.png){: w="600"}

![Pasted image 20241120191956](/assets/Image/Pasted image 20241120191956.png){: w="500"}

we have **CONFLICTING** demands for a block. The word at address 18 ($10010_2$) should be brought into cache block 2 ($010_2$). Hence, it must **REPLACE** the word at address 26 ($11010_2$), which is already in cache block 2 ($010_2$). This behavior allows a cache to take advantage of **temporal locality**: recently referenced words replace less recently referenced words.

**只有当输入地址完全一样时才算命中，仅仅是mod 8后的地址，即在cache块地址相同，而输入地址不同，也是miss！**比如10010和11010


#### 3-2  Diagram

![Pasted image 20241121134443](/assets/Image/Pasted image 20241121134443.png)

**Notation**
	
1. The **TAG** from the cache is compared against the **upper portion of the address** to determine whether the **entry('entry' means 'line' in cache)** in the cache corresponds to the requested address
2. Because the cache has $2^{10}$ (or 1024) entries and a **block size** of 1 word, 10 bits are used to index the cache, leaving 64 − 10 − 2 = 52 bits to be compared against the tag


#### 3-3  Size of Cache (in bits)

##### Formula
![Pasted image 20241121170723](/assets/Image/Pasted image 20241121170723.png)

##### Notation
1. **n**: The cache size is $2^n$ blocks, so `n` indicates how many bits the `Index` field has.
2. **m**: The block size is $2^m$ **words**, ($2^{m}×4$ **bytes**--$2^{m}×32$ **bits**). Hence `m` indicates how many bits the `Offset` field has.
3. **2**: two bits used for the byte part of the address
4. (64-m-n-2): the `tag` field. This method of calculating the bits number  in tag field uses the ADDRESS's tag field.(the two tag fileds are same in bits)
5. **1**: `valid bit`

>So, $2^n$ is the number of entries(or lines, vividly). And ($2^m$×32+(64-n-m-2)+1) is the TOTAL numbers of bits of [Data, Tag and Valid bit] in a single entry.
>The product of these two things is the SIZE of Cache(in bits).

---
##### Distinguish
> [!NOTE] Data, Tag and Valid bit
> When we saty 'block', we just means the field of Data. 
> But a signle entry in cache consists of not only the data filed, but tag and valid bit.
> 
> **The total size of a single entry = data + tag +valid bits**
>

| tag | index | offset |
| --- | ----- | ------ |
↑ structure of an **address**

| valid bit | tag | data(a.k.a `block`) |
| --------- | --- | ------------------- |
↑ structure of an **entry** in cache

---
#### 3-5  KiB v.s KB

- 1KB = $10^3$ = 1000 Byte
- 1MB = $10^6$ = 1000*1000 Byte = 1000KB

- 1KiB = 2^10 = 1024 Byte
- 1MiB = 2^20 = 1024*1024 Byte = 1024KiB

#### 3-6  Examples

###### e.g.1 Cache Size
![Pasted image 20241121174928](/assets/Image/Pasted image 20241121174928.png){: w="600"}

###### e.g.2 Byte address -- Number of block
![Pasted image 20241121175019](/assets/Image/Pasted image 20241121175019.png){: w="600"}

####  3-7 辨析

##### **1. `Byte Offset` 的作用是什么？**

`Byte Offset` 用于确定在一个 **Cache 行（Cache Block）** 中的具体字节位置。

- Cache 通常以 **块（Block）** 为单位存储数据，而每个块可能包含多个字节（例如 16 字节或 64 字节）。
- 当从主存加载一个块到 Cache 时，整个块会被加载，但 CPU 可能只需要其中的一部分数据（如一个字或一个字节）。`Byte Offset` 用于精确定位该块中具体需要的数据字节。

在图中：

- `Byte Offset` 是地址的最低位（如图所示为 2 位）。
- 它指定了一个块（例如 4 字节块）中的具体字节位置：
    - 00 表示第 0 个字节。
    - 01 表示第 1 个字节。
    - 10 表示第 2 个字节。
    - 11 表示第 3 个字节。

---

##### **2. `Byte Offset` 是否总是 2 位？**

**不一定，总位数取决于块的大小。**

- **块大小（Block Size）** 决定了 `Byte Offset` 所需的位数：
    - 如果块是 4 字节：需要 2 位（因为 22=42^2 = 422=4）。
    - 如果块是 8 字节：需要 3 位（因为 23=82^3 = 823=8）。
    - 如果块是 16 字节：需要 4 位（因为 24=162^4 = 1624=16）。


---

##### **3. 我们从 Cache 中取数据时，是取一个字节还是整个块？**

**从 Cache 中加载数据时：**

- **实际上是**整个块**被加载到 Cache 中**。这符合 Cache 设计中基于**空间局部性**的原理（即临近的数据可能也会被访问）。
- **但 CPU 最终只取需要的字节或字**（比如 32 位字或 64 位字），通过 `Byte Offset` 精确定位。

---

##### **4. `Block` 和 `Entry` 有什么区别？**

两者有一定关系，但意义不同：

###### **Block（块）：**

- **Block 是 Cache 存储的最小单位**，它是一段从主存加载到 Cache 的连续数据（如 16 字节或 64 字节）。
- 块大小是系统设计中的固定参数。
- 块内部数据通过 `Byte Offset` 精确定位。

###### **Entry（条目）：**

- **Entry 是 Cache 中的一个存储单元**，包括一个块和相关的元信息（如 Valid 位和 Tag）。
- 每个 Entry 通常存储：
    - 一个块（Block）。
    - 该块的 `Tag`（用于标识主存地址）。
    - 有效位（Valid Bit）、脏位（Dirty Bit）等。
- 如果是组相联或直接映射 Cache，Entry 还会有 `Index` 用于定位。

**区别总结：**

- Block 是存储的实际数据内容，Entry 包含 Block 和管理该块的元信息。

####  3-8  Miss Ratio

![Pasted image 20241121193136](/assets/Image/Pasted image 20241121193136.png){: w="500"}

>**Larger blocks** exploit spatial locality to **lower miss rates**. 
>But below are the drawbacks.

（1）
As Figure 5.11 shows, increasing the block size USUALLY `decreases the miss rate`. 
	
BUT: 
>The miss rate may **GO UP** if the block size becomes **TOO LARGE**.
	
That's because, the **number of blocks that can be held in the cache** will become `small`, and there will be a great deal of `competition` for those blocks. As a result, a block will be `bumped out of the cache `before many of its words are accessed.
	
Stated alternatively, **spatial locality** `decreases` with a **very large block**; consequently, the benefits to the miss rate become smaller.

（2）
>Another problem associated with increasing the block size is that the **miss  penalty rises**.
- miss penalty：the time required to fetch the block from the next lower level and load it into the cache.
	
The time has two parts: the latency to the first word and the **`transfer time`** for the rest of the block. Clearly, unless we change the memory system, **the TRANSFER TIME—and hence the miss penalty—will `increase` as the block size expands.** 
	
Furthermore, the improvement in the miss rate starts to decrease as the blocks become larger. The result is that **the `increase` in the miss penalty OVERWELMS the `decrease` in the miss rate for blocks that are too large, and cache performance thus `decreases`.**

### Part IV:  **Handling Cache Misses**

Remember that cache is divided into 2 parts( `instruction cache` and `data cache`)?

##### 1) Steps to handle **instruction** cache miss:
	
1. Send the original `PC` value to the memory.
2. Instruct `main memory` to perform a **read**, and **wait** for the memory to
complete its access.
3. `Write the cache entry`, putting the data from memory in the data portion of
the entry, writing the upper bits of the address (from the ALU) into the `tag` field, and turning the `valid bit` on.
4. `Restart the instruction execution at the first step`, which will refetch the
instruction, this time finding it in the cache.

##### 2) Steps to handle **data** cache miss: 
	
The control of the cache on a data access is essentially identical: on a miss, we
simply stall the processor until the memory responds with the data.

### Part V:  **Handling Writes**

#### 5-1  write-back & Inconsistent

**write back**是一种写策略：处理写操作时，只更新cache中对应的block。当该block被替换时，再将更新后的block写入下一级存储。

After `writing` the `cache`, `main memory` would have a **different value from that in the cache.**
	In such a case, the cache and memory are said to be inconsistent.
（在写回(wtire-**back**)策略下，数据的修改仅发生在cache中，而不会立刻更新到主存中。只有当cache中的数据块被替换（evicted）时，系统才会将修改后的数据写回主存。）
####  5-2 write-through

在直写(write-**through**)策略下，每次对cache的数据进行修改时，系统同时将修改写入主存，保证cache和主存中的数据始终一致。

虽然上述设计方案能够简单地处理写操作，但是它的性能不佳。基于写穿透策略，每次的写操作都会引起写主存的操作。这些写操作延时很长，会大大降低处理器的性能。

#### 5-3  write-buffer
我们采用写缓冲(write buffer)来解决问题。write buffer是一个**保存着等待写入主存的数据的队列**
	
数据写入cache的同时也**写入写缓冲中**，之后处理器继续执行；当写入主存的操作完成后，写缓冲中的表项将被释放；
	
如果写缓冲满了，处理器必须**停顿**流水线，直到write buffer中出现空闲表项；