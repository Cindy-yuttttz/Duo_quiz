#!/usr/bin/env python3
"""save_snapshot.py — 保存当前 index.html 的快照"""
import sys, os, json, shutil, re
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(BASE, "index.html")
VER_DIR = os.path.join(BASE, ".versions")
META = os.path.join(VER_DIR, "versions.json")

if not os.path.exists(HTML):
    print(f"❌ 未找到 {HTML}")
    sys.exit(1)

label = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "unspecified"
slug = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff_-]', '-', label)[:40].strip('-').lower() or 'no-label'

# 读取已有元数据
if os.path.exists(META):
    with open(META, encoding='utf-8') as f:
        versions = json.load(f)
else:
    versions = []

# 计算下一个版本号
next_num = max([v.get("num", 0) for v in versions], default=0) + 1
ts = datetime.now().strftime("%Y%m%d-%H%M%S")
filename = f"v{next_num}-{ts}-{slug}.html"
dest = os.path.join(VER_DIR, filename)

shutil.copy2(HTML, dest)

entry = {
    "num": next_num,
    "file": filename,
    "label": label,
    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "size": os.path.getsize(dest)
}
versions.append(entry)

with open(META, 'w', encoding='utf-8') as f:
    json.dump(versions, f, ensure_ascii=False, indent=2)

# 更新 latest 软链接
latest_link = os.path.join(VER_DIR, "latest.html")
if os.path.islink(latest_link) or os.path.exists(latest_link):
    os.remove(latest_link)
os.symlink(filename, latest_link)

print(f"✅ 已保存 v{next_num}: {filename} ({entry['label']})")
