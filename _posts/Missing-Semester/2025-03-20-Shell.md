---
title: "shell"
date: 2025-03-20 03:39:16 +0800
categories: [Missing-Semester]
math: true
---

## 文件处理
---
1. `mkdir ...`: 创建目录
2. `rm ...`: 删除目录
3. `touch ...`: 创建文件
4. `echo "..." > ...`: 向文件写入（
	```bash
   echo "Some text" > file.txt     # 创建新文件或覆盖已有文件
   echo "More text" >> file.txt    # 追加到文件末尾
   ```
5. `cat`查看文件内容
6. `./`: 执行文件,与文件名中间**不能加空格**
7. `chmod`: 改变文件或目录的访问权限
```bash
$ ./semester 
-bash: ./: Is a directory #无执行权限
```

## 管道`|`与重定向`>`
---
将 `semester` 文件输出的last-modified一行信息,写入主目录下的 `last-modified.txt` 的文件中：
```bash
./semester | grep -i "Last-Modified" > ~/last-modified.txt
```
- `./semester` 执行脚本，获取 HTTP 头信息
- `|` 将输出传递给下一个命令
- `grep -i "Last-Modified"` 过滤出包含 "Last-Modified" 的行（-i 表示忽略大小写）
- `> ~/last-modified.txt` 将结果重定向到主目录下的 last-modified.txt 文件