# Obsidian 到 Chirpy 转换工具

这些工具可以自动修复 Obsidian 笔记在 Chirpy 博客主题中的兼容性问题，实现一劳永逸的解决方案。


### 一键修复格式

```bash
# 在博客根目录运行
chmod +x tools/quick_fix.sh
./tools/quick_fix.sh
```


#### 🔧 修复的问题

##### 1. 图片语法转换
- **原格式**: `![[image.png]]` 或 `![[image.png|500]]`
- **转换为**: `![image](/assets/Image/image.png)` 或 `![image](/assets/Image/image.png){: w="500"}`

##### 2. 数学公式支持
- 自动检测包含数学公式的文章
- 为其添加 `math: true` 配置
- 支持行内公式 `$...$` 和块级公式 `$$...$$`

##### 3. 其他 Obsidian 语法
- 内部链接：`[[链接]]` → `[链接](/posts/链接/)`
- 高亮文本：`==文本==` → `**文本**`

### 📝 新文章写作流程

1. **在 Obsidian 中正常写作**
2. **复制内容到 Jekyll 文章文件**
3. **运行修复脚本**（可选，已配置全局默认值）
   ```bash
   ./tools/quick_fix.sh
   ```
4. **预览和发布**
   ```bash
   bundle exec jekyll serve
   git add . && git commit -m "新增文章" && git push
   `
---

### 自动添加规范的frontmatter：
`python3 auto_frontmatter.py`