#!/usr/bin/env python3
"""list_versions.py — 列出所有版本"""
import os, json, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
META = os.path.join(BASE, ".versions", "versions.json")
VER_DIR = os.path.join(BASE, ".versions")

if not os.path.exists(META):
    print("📭 还没有版本记录")
    sys.exit(0)

with open(META, encoding='utf-8') as f:
    versions = json.load(f)

if not versions:
    print("📭 版本列表为空")
    sys.exit(0)

current_size = os.path.getsize(os.path.join(BASE, "index.html")) if os.path.exists(os.path.join(BASE, "index.html")) else 0

print(f"{'':─<60}")
print(f"  多儿出警 版本历史  (共 {len(versions)} 个版本)")
print(f"{'':─<60}")
print(f"  {'版本':<6} {'时间':<18} {'大小':<8} {'描述'}")
print(f"{'':─<60}")
for v in versions:
    marker = " ← 当前" if v.get("size") == current_size and v == versions[-1] else ""
    size_str = f"{v['size']/1024:.0f}KB" if v['size'] > 0 else "?"
    print(f"  v{v['num']:<4} {v['time']:<16} {size_str:<6} {v['label']}{marker}")

print(f"{'':─<60}")
print(f"  版本文件目录: {VER_DIR}")
print(f"  使用: python3 restore_version.py v{{N}} 来回滚")
print(f"{'':─<60}")
