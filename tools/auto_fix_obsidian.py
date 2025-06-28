#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Obsidian 到 Chirpy 语法自动转换工具
一劳永逸解决 Obsidian 语法兼容性问题

使用方法：
python3 tools/auto_fix_obsidian.py [目标目录]

功能：
1. 转换图片语法：![[image.png]] -> ![alt](/assets/Image/image.png)
2. 自动添加 math: true（如果检测到数学公式）
3. 修复常见的 Obsidian 语法问题
4. 生成修复报告
"""

import os
import re
import glob
import argparse
from pathlib import Path
from datetime import datetime

class ObsidianToChirpyConverter:
    def __init__(self, target_dir="_posts"):
        self.target_dir = target_dir
        self.stats = {
            'total_files': 0,
            'modified_files': 0,
            'images_fixed': 0,
            'math_enabled': 0,
            'errors': []
        }
    
    def has_math_formula(self, content):
        """检测内容是否包含数学公式"""
        math_patterns = [
            r'\$[^$\n]+\$',           # 行内公式 $...$
            r'\$\$[\s\S]*?\$\$',      # 块级公式 $$...$$
            r'\\[(\w+)]{',            # LaTeX 命令 \mathbf{}, \frac{}, etc.
            r'\\begin{.*?}',          # LaTeX 环境
            r'\\[a-zA-Z]+\s*\{',     # 其他 LaTeX 命令
        ]
        
        for pattern in math_patterns:
            if re.search(pattern, content):
                return True
        return False
    
    def fix_image_syntax(self, content):
        """修复 Obsidian 图片语法"""
        def replace_image(match):
            full_match = match.group(0)
            image_path = match.group(1)
            
            # 提取图片名称作为 alt 文本
            image_name = Path(image_path).stem
            alt_text = image_name.replace('_', ' ').replace('-', ' ')
            
            # 检查是否有尺寸参数
            if '|' in image_path:
                image_path, size_params = image_path.split('|', 1)
                # 解析尺寸参数
                if 'x' in size_params:
                    try:
                        width, height = size_params.split('x')
                        return f'![{alt_text}](/assets/Image/{image_path}){{: w="{width.strip()}" h="{height.strip()}"}}'
                    except:
                        pass
                else:
                    # 只有宽度
                    return f'![{alt_text}](/assets/Image/{image_path}){{: w="{size_params.strip()}"}}'
            
            return f'![{alt_text}](/assets/Image/{image_path})'
        
        # 匹配 Obsidian 图片语法
        pattern = r'!\[\[([^\]]+)\]\]'
        original_count = len(re.findall(pattern, content))
        new_content = re.sub(pattern, replace_image, content)
        fixed_count = original_count - len(re.findall(pattern, new_content))
        
        self.stats['images_fixed'] += fixed_count
        return new_content, fixed_count > 0
    
    def add_math_config(self, content):
        """如果检测到数学公式且缺少 math 配置，则添加"""
        if not self.has_math_formula(content):
            return content, False
        
        if 'math:' in content:
            return content, False  # 已有 math 配置
        
        lines = content.split('\n')
        if len(lines) < 3 or lines[0] != '---':
            return content, False  # 无有效 front matter
        
        # 找到第二个 --- 的位置
        end_index = -1
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == '---':
                end_index = i
                break
        
        if end_index == -1:
            return content, False  # front matter 格式错误
        
        # 在 --- 前添加 math: true
        lines.insert(end_index, 'math: true')
        self.stats['math_enabled'] += 1
        return '\n'.join(lines), True
    
    def fix_common_obsidian_syntax(self, content):
        """修复其他常见的 Obsidian 语法问题"""
        modified = False
        
        # 修复内部链接 [[链接]] -> [链接](/posts/链接/)
        internal_link_pattern = r'\[\[([^\]]+)\]\]'
        if re.search(internal_link_pattern, content):
            def replace_internal_link(match):
                link_text = match.group(1)
                # 简单处理：转换为相对链接
                return f'[{link_text}](/posts/{link_text}/)'
            
            content = re.sub(internal_link_pattern, replace_internal_link, content)
            modified = True
        
        # 修复高亮语法 ==文本== -> **文本**
        highlight_pattern = r'==([^=]+)=='
        if re.search(highlight_pattern, content):
            content = re.sub(highlight_pattern, r'**\1**', content)
            modified = True
        
        return content, modified
    
    def process_file(self, file_path):
        """处理单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            content = original_content
            file_modified = False
            
            # 1. 修复图片语法
            content, img_fixed = self.fix_image_syntax(content)
            if img_fixed:
                file_modified = True
            
            # 2. 添加数学公式配置
            content, math_added = self.add_math_config(content)
            if math_added:
                file_modified = True
            
            # 3. 修复其他 Obsidian 语法
            content, other_fixed = self.fix_common_obsidian_syntax(content)
            if other_fixed:
                file_modified = True
            
            # 如果有修改，保存文件
            if file_modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.stats['modified_files'] += 1
                print(f"✓ 修复: {file_path}")
            else:
                print(f"- 跳过: {file_path}")
            
        except Exception as e:
            error_msg = f"处理 {file_path} 时出错: {e}"
            self.stats['errors'].append(error_msg)
            print(f"✗ {error_msg}")
    
    def process_directory(self):
        """处理整个目录"""
        print(f"开始处理目录: {self.target_dir}")
        print("=" * 50)
        
        # 查找所有 markdown 文件
        md_files = glob.glob(f"{self.target_dir}/**/*.md", recursive=True)
        self.stats['total_files'] = len(md_files)
        
        for file_path in md_files:
            self.process_file(file_path)
        
        self.print_summary()
    
    def print_summary(self):
        """打印处理摘要"""
        print("\n" + "=" * 50)
        print("🎉 处理完成！修复摘要:")
        print(f"📁 总文件数: {self.stats['total_files']}")
        print(f"✅ 修改文件数: {self.stats['modified_files']}")
        print(f"🖼️  修复图片数: {self.stats['images_fixed']}")
        print(f"🔢 启用数学公式: {self.stats['math_enabled']}")
        
        if self.stats['errors']:
            print(f"❌ 错误数: {len(self.stats['errors'])}")
            for error in self.stats['errors']:
                print(f"   - {error}")
        
        print(f"\n⏰ 处理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    parser = argparse.ArgumentParser(description='Obsidian 到 Chirpy 语法自动转换工具')
    parser.add_argument('target_dir', nargs='?', default='_posts', 
                       help='目标目录 (默认: _posts)')
    parser.add_argument('--dry-run', action='store_true', 
                       help='预览模式，不实际修改文件')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.target_dir):
        print(f"❌ 目录不存在: {args.target_dir}")
        return
    
    print("🔧 Obsidian 到 Chirpy 语法自动转换工具")
    print(f"📂 目标目录: {args.target_dir}")
    
    if args.dry_run:
        print("🔍 预览模式 - 不会实际修改文件")
    
    print()
    
    converter = ObsidianToChirpyConverter(args.target_dir)
    converter.process_directory()

if __name__ == "__main__":
    main() 