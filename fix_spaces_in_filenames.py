#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

def fix_spaces_in_filenames():
    """修复文件名中的空格问题"""
    posts_dir = Path('_posts')
    
    if not posts_dir.exists():
        print("❌ 错误: _posts目录不存在")
        return
    
    # 找到所有包含空格的.md文件
    files_with_spaces = []
    for file_path in posts_dir.glob('*.md'):
        if ' ' in file_path.name:
            files_with_spaces.append(file_path)
    
    print(f"📁 找到 {len(files_with_spaces)} 个文件名包含空格的文件")
    
    if not files_with_spaces:
        print("✅ 没有需要修复的文件")
        return
    
    print("-" * 60)
    
    fixed_count = 0
    for file_path in files_with_spaces:
        old_name = file_path.name
        # 将空格替换为连字符
        new_name = old_name.replace(' ', '-')
        new_path = file_path.parent / new_name
        
        try:
            file_path.rename(new_path)
            print(f"📝 重命名: {old_name} → {new_name}")
            fixed_count += 1
        except Exception as e:
            print(f"❌ 重命名失败 {old_name}: {e}")
    
    print("-" * 60)
    print(f"🎉 处理完成! 共修复了 {fixed_count} 个文件")

if __name__ == "__main__":
    fix_spaces_in_filenames() 