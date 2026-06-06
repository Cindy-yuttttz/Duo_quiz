#!/usr/bin/env python3
"""restore_version.py — 回滚到指定版本"""
import os, json, sys, shutil
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(BASE, "index.html")
VER_DIR = os.path.join(BASE, ".versions")
META = os.path.join(VER_DIR, "versions.json")

if len(sys.argv) < 2:
    print("用法: python3 restore_version.py v3")
    sys.exit(1)

v_id = sys.argv[1].lstrip("v")

with open(META, encoding='utf-8') as f:
    versions = json.load(f)

target = None
for v in versions:
    if str(v["num"]) == v_id:
        target = v
        break

if not target:
    print(f"❌ 未找到版本 v{v_id}")
    print("可用版本: " + ", ".join(f"v{v['num']}" for v in versions))
    sys.exit(1)

src = os.path.join(VER_DIR, target["file"])
if not os.path.exists(src):
    print(f"❌ 版本文件不存在: {src}")
    sys.exit(1)

# 备份当前版本
ts = datetime.now().strftime("%Y%m%d-%H%M%S")
backup_file = f"rollback-{ts}.html"
backup_path = os.path.join(VER_DIR, backup_file)
shutil.copy2(HTML, backup_path)

# 恢复目标版本
shutil.copy2(src, HTML)

rollback_entry = {
    "num": len(versions) + 1,
    "file": backup_file,
    "label": f"↩️ 回滚到 v{target['num']}（备份）",
    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "size": os.path.getsize(backup_path),
    "rollback_from": target["file"]
}
versions.append(rollback_entry)

with open(META, 'w', encoding='utf-8') as f:
    json.dump(versions, f, ensure_ascii=False, indent=2)

# 更新 latest 软链接
latest_link = os.path.join(VER_DIR, "latest.html")
if os.path.islink(latest_link) or os.path.exists(latest_link):
    os.remove(latest_link)
os.symlink(target["file"], latest_link)

print(f"✅ 已回滚到 v{target['num']}: {target['label']}")
print(f"  当前版本已备份为: {backup_file}")
print(f"  HTTP 服务器无需重启，立即生效")
