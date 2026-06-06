#!/usr/bin/env python3
"""diff_versions.py — 比较两个版本的差异"""
import os, json, sys, difflib

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VER_DIR = os.path.join(BASE, ".versions")
META = os.path.join(VER_DIR, "versions.json")

def get_file(v_id):
    """根据 v{N} 或 'current' 返回 (标签, 文件路径)"""
    if v_id == "current":
        return "当前", os.path.join(BASE, "index.html")
    with open(META, encoding='utf-8') as f:
        versions = json.load(f)
    target = v_id.lstrip("v")
    for v in versions:
        if str(v["num"]) == target:
            return f"v{v['num']} ({v['label']})", os.path.join(VER_DIR, v["file"])
    print(f"❌ 未找到版本 {v_id}")
    sys.exit(1)

if len(sys.argv) < 3:
    print("用法: python3 diff_versions.py v1 v2")
    print("      python3 diff_versions.py current v3")
    sys.exit(1)

label_a, path_a = get_file(sys.argv[1])
label_b, path_b = get_file(sys.argv[2])

with open(path_a, encoding='utf-8') as f:
    lines_a = f.readlines()
with open(path_b, encoding='utf-8') as f:
    lines_b = f.readlines()

diff = list(difflib.unified_diff(lines_a, lines_b, fromfile=label_a, tofile=label_b, n=3))

# 过滤掉只有时间戳/URL不同的噪音行
significant = [l for l in diff
               if not l.startswith('---') and not l.startswith('+++')
               and 'QUIZ_URL' not in l
               and 'trycloudflare.com' not in l
               and 'const QUIZ_URL' not in l]

if not significant:
    print(f"✅ {label_a} 和 {label_b} 没有显著差异（仅URL变动已过滤）")
    sys.exit(0)

print(f"📊 差异: {label_a} ↔ {label_b}")
print(f"{'':─<50}")
print(f"  改动了 {sum(1 for l in significant if l.startswith('+'))} 处增加, "
      f"{sum(1 for l in significant if l.startswith('-'))} 处删除")
print(f"{'':─<50}")
for line in significant:
    sys.stdout.write(line)
