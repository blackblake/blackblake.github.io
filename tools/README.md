# Obsidian 到 Chirpy 转换工具

这些工具可以自动修复 Obsidian 笔记在 Chirpy 博客主题中的兼容性问题，实现一劳永逸的解决方案。

## 🚀 快速开始

### 方法1：一键修复（推荐）
```bash
# 在博客根目录运行
chmod +x tools/quick_fix.sh
./tools/quick_fix.sh
```

### 方法2：使用 Python 脚本
```bash
# 修复所有文件
python3 tools/auto_fix_obsidian.py

# 只修复特定目录
python3 tools/auto_fix_obsidian.py _posts/MARL

# 预览模式（不实际修改文件）
python3 tools/auto_fix_obsidian.py --dry-run
```

## 🔧 修复的问题

### 1. 图片语法转换
- **原格式**: `![[image.png]]` 或 `![[image.png|500]]`
- **转换为**: `![image](/assets/Image/image.png)` 或 `![image](/assets/Image/image.png){: w="500"}`

### 2. 数学公式支持
- 自动检测包含数学公式的文章
- 为其添加 `math: true` 配置
- 支持行内公式 `$...$` 和块级公式 `$$...$$`

### 3. 其他 Obsidian 语法
- 内部链接：`[[链接]]` → `[链接](/posts/链接/)`
- 高亮文本：`==文本==` → `**文本**`

## ⚙️ 全局配置（一劳永逸）

我已经为您在 `_config.yml` 中添加了默认配置：

```yaml
defaults:
  - scope:
      path: ""
      type: posts
    values:
      math: true  # 自动为所有新文章启用数学公式
```

这意味着：
- ✅ 以后所有新文章都会自动启用数学公式支持
- ✅ 不需要手动添加 `math: true`
- ✅ 直接从 Obsidian 复制粘贴数学公式即可

## 📝 新文章写作流程

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
   ```

## 🎯 脚本详细功能

### `auto_fix_obsidian.py`
- 全功能转换脚本
- 支持批量处理
- 生成详细报告
- 支持预览模式

### `quick_fix.sh`
- 一键修复脚本
- 适合日常使用
- 自动处理常见问题

## ⚠️ 注意事项

1. **图片文件位置**: 确保图片文件放在 `assets/Image/` 目录下
2. **备份重要文件**: 首次使用前建议备份重要文章
3. **预览检查**: 修复后建议本地预览检查效果

## 🆘 常见问题

**Q: 数学公式还是不显示？**
A: 检查 front matter 中是否有 `math: true`，或重新运行修复脚本

**Q: 图片显示不出来？**
A: 确认图片文件在 `assets/Image/` 目录下，文件名与引用一致

**Q: 可以只修复特定文件吗？**
A: 可以，使用 `python3 tools/auto_fix_obsidian.py 文件路径`

## 🔄 未来维护

只需要：
1. 继续在 Obsidian 中写作
2. 偶尔运行 `./tools/quick_fix.sh` 修复新问题
3. 新文章的数学公式会自动启用（已配置全局默认值）

---

现在您可以专注于写作，而不用担心语法兼容性问题！ 🎉 