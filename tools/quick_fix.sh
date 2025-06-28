#!/bin/bash
# Obsidian 到 Chirpy 快速修复脚本
# 一键修复所有常见的兼容性问题

echo "🔧 Obsidian 到 Chirpy 快速修复脚本"
echo "=================================="

# 检查是否在正确的目录
if [ ! -d "_posts" ]; then
    echo "❌ 错误：请在博客根目录运行此脚本"
    exit 1
fi

echo "📂 开始修复 _posts 目录下的文件..."

# 1. 修复图片语法：![[image.png]] -> ![image](/assets/Image/image.png)
echo "🖼️  修复 Obsidian 图片语法..."
find _posts -name "*.md" -exec sed -i '' 's/!\[\[\([^]]*\)\]\]/![图片](\/assets\/Image\/\1)/g' {} \;

# 2. 为包含数学公式的文件添加 math: true
echo "🔢 检查数学公式，添加 math 配置..."
python3 tools/auto_fix_obsidian.py

# 3. 检查并创建 assets/Image 目录
if [ ! -d "assets/Image" ]; then
    echo "📁 创建 assets/Image 目录..."
    mkdir -p assets/Image
fi

echo ""
echo "✅ 修复完成！"
echo "🚀 现在您可以运行 'bundle exec jekyll serve' 来预览博客"
echo "📤 或者运行 'git add . && git commit -m \"修复Obsidian语法\" && git push' 来发布" 