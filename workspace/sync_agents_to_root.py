# -*- coding: utf-8 -*-
"""Sync AGENTS.md from workspace to root"""
import os

src = r"d:\OpenClaw\workspace\AGENTS.md"
dst = r"d:\OpenClaw\AGENTS.md"

with open(dst, 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = "## 🛠️ Available Tools"
end_marker = "## Forbidden Phrases"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    with open(src, 'r', encoding='utf-8') as f:
        src_content = f.read()
    
    src_start = src_content.find(start_marker)
    src_end = src_content.find(end_marker)
    
    if src_start != -1 and src_end != -1:
        new_section = src_content[src_start:src_end]
        new_content = content[:start_idx] + new_section + content[end_idx:]
        
        with open(dst, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✅ Root AGENTS.md also updated!")
    else:
        print("❌ Source section not found")
else:
    print("ℹ️ Root AGENTS.md has different structure, skipping")
