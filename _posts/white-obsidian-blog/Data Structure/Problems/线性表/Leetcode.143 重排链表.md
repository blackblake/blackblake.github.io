---
title: lc143.重拍链表
categories:
  - DSA
  - list
---
## 官方题解

---
[讲解视频](https://www.bilibili.com/video/BV1KG4y1G7cu/?vd_source=0d49e59abf4b8220ef3a25c5822e3a13)

```cpp
class Solution {
    // 876. 链表的中间结点
    ListNode *middleNode(ListNode *head) {
        ListNode *slow = head, *fast = head;
        while (fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
        }
        return slow;
    }

    // 206. 反转链表
    ListNode *reverseList(ListNode *head) {
        ListNode *pre = nullptr, *cur = head;
        while (cur) {
            ListNode *nxt = cur->next;
            cur->next = pre;
            pre = cur;
            cur = nxt;
        }
        return pre;
    }

public:
	//合并head和head2链表
    void reorderList(ListNode *head) {
        ListNode *mid = middleNode(head);
        ListNode *head2 = reverseList(mid);
        while (head2->next) {
            ListNode *nxt = head->next;
            ListNode *nxt2 = head2->next;
            head->next = head2;
            head2->next = nxt;
            head = nxt;
            head2 = nxt2;
        }
    }
};

```

## 主要内容
---
#### (1)快慢指针法找中间节点

```cpp
		ListNode* slow=head;
        ListNode* fast=head;

        while(fast&&fast->next){

            slow=slow->next;
            fast=fast->next->next;

        }//结束后slow指向中间节点
```

#### (2)反转链表

```cpp
ListNode* reverseList(ListNode* head) {
        ListNode* prev = nullptr;
        ListNode* curr = head;
        while (curr) {
            ListNode* next = curr->next;//保存next
            
            curr->next = prev;//这一句是主要操作,其他3句是准备工作
            //prev的值在上一轮循环确定,是上一轮的"curr"
            
            prev = curr;//更新prev
            curr = next;//更新curr
        }
        return prev;
    }

```

## 经验
---

> [!NOTE] 经验
> 1. 一定要在开始写代码之前构思好，画好示意图。别一想到可行的方法就写。要想想，有没有更好写、更容易实现的（即使时间复杂度高也没关系）
>    
> 2. 一个很好的想法：由于此题输入结点的顺序是不按顺序来的，所以在循环中，当前结点的下一个结点可能还没有出现过，这就需要先把这些结点及其数据存放起来，待全部输入完后再连接。我这里用了一个 **vector<ListNode*> listVec(num);** 来存储，这个方法蛮好
>    
> 3. 但是要注意，**vector创建的时候一定要写好结点数“listVec(num)”，否则无法加入元素！！**

