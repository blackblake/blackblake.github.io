---
title: proj1
categories:
  - cs61b
---
## LinkedList Double-end Queue
---
### 1️⃣Generics in Java

```java
public class LinkedListDeque <T> {  
    //结点类Node作为'内部类'嵌套在LinkedListDeque类里面
    private class LinkNode{  
        T item;  
        LinkNode prev;  
        ...
    }  
}
```
