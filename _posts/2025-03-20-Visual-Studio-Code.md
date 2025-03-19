---
title: vs configuration
date: 2025-03-20 03:39:16 +0800
categories: [Tool, Visual Studio Code]
tags: [config]     # TAG names should always be lowercase
---
![[截屏2025-03-07 21.30.53.png]]

### 遇到的问题：
---
按下`command+shift+B`编译，或右上角的三角形`run`按钮后，都只会在终端显示：

```bash
生成已成功完成
Terminal will be reused by tasks, press any key to close it.
```

如果我想输入cin的n和m等数字，终端就会立即关闭。这是因为上面👆的信息含义是“**编译**”成功了，而不是开始运行了，我也不清楚为什么点击run按钮却不能运行

### 解决方案暂时为：
---
先用`command+shift+B`编译，然后按下`+`号开启一个`zsh`终端，在这里输入`./acwing795`来运行即可

### 补充：
---
如上图所示，右边的小窗口是一个外部控制台，我通过在`launch.json`里添加一条

```json
"externalConsole": true
```

从而开启这个外部控制台，当调试的时候就能在这个外部控制台输入需要输入的数据，输入会同步到vscode的调试窗口
