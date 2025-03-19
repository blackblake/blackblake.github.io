---
title: lec3
categories:
  - cs61b
---
==这一讲是重点，多看几遍slides==
## Junit
---
JUnit 输出的信息有点难看，手动调用每个测试也很烦人

### 新语法 #1
1. 用 **\@org.junit.Test** 来注解每个测试
2. 将所有测试方法改为 **non-static** 方法
3. 使用 JUnit 运行程序运行所有测试并将结果列表化
- IntelliJ 提供了默认的运行程序/渲染器, 确定删除 main
- 使Junit输出更易于阅读，无需手动调用测试！

### 新语法 #2
重复键入库名是很烦人的，例如 `org.junit.Test` 和 `org.junit.Assert.assertEquals`

可以在每个测试文件的开头使用
```java
import org.junit.Test.Assert.assertEquals
import static org.junit.Assert.*；
```

这将神奇地消除输入 "org.junit "或 "org.junit.Assert "的需要

## Helper Method -- how to manage complexity
---
![[Pasted image 20250228190249.png]]

测试提供稳定性和脚手架, 增强对基本单元的信心, 减少打破单元的可能性, 帮助您一次只专注于一项任务. 
