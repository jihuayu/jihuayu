#!/usr/bin/env python3
import subprocess
import json
import datetime
import sys
from datetime import datetime, timezone

# 获取所有的fork仓库
try:
    result = subprocess.run(
        ['gh', 'repo', 'list', '--json', 'name,pushedAt,isFork', '--limit', '1000'],
        capture_output=True, text=True, check=True
    )
    repos = json.loads(result.stdout)
except subprocess.CalledProcessError as e:
    print(f"执行gh命令失败: {e.stderr}")
    sys.exit(1)
except json.JSONDecodeError:
    print("解析GitHub响应失败")
    sys.exit(1)

# 当前时间
now = datetime.now(timezone.utc)

# 筛选一个月内没有活动的fork仓库
inactive_forks = []
for repo in repos:
    if repo['isFork']:
        pushed_at = datetime.fromisoformat(repo['pushedAt'].replace('Z', '+00:00'))
        days_since_push = (now - pushed_at).days
        
        if days_since_push > 30:  # 超过30天没有活动
            inactive_forks.append(repo['name'])

# 将结果写入repo.txt
with open('repo.txt', 'w') as f:
    for repo_name in inactive_forks:
        f.write(f"{repo_name}\n")

# 输出结果
print(f"找到{len(inactive_forks)}个超过一个月未活跃的fork仓库，已保存到repo.txt")