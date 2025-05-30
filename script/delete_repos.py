#!/usr/bin/env python3
import subprocess
import sys
import time
import os

# 检查repo.txt是否存在
if not os.path.exists('repo.txt'):
    print("错误: repo.txt 文件不存在！")
    sys.exit(1)

# 读取repo.txt中的仓库列表
with open('repo.txt', 'r') as f:
    repos = [line.strip() for line in f if line.strip()]

if not repos:
    print("repo.txt 中没有仓库名称，无需执行删除操作。")
    sys.exit(0)

# 确认操作
print(f"将要删除以下 {len(repos)} 个仓库:")
for repo in repos:
    print(f"- {repo}")
confirmation = input("\n这是一个不可逆操作！请输入 'yes' 确认删除这些仓库: ")

if confirmation.lower() != 'yes':
    print("操作已取消。")
    sys.exit(0)

# 开始删除仓库
deleted_count = 0
failed_repos = []

for repo in repos:
    print(f"\n正在删除仓库: {repo}")
    try:
        # 使用gh命令删除仓库
        result = subprocess.run(
            ['gh', 'repo', 'delete', '--yes', repo],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            print(f"✅ 成功删除仓库: {repo}")
            deleted_count += 1
        else:
            print(f"❌ 删除仓库失败: {repo}")
            print(f"错误信息: {result.stderr}")
            failed_repos.append(repo)
        
        # 添加短暂延迟避免触发GitHub API限制
        time.sleep(1)
    
    except Exception as e:
        print(f"❌ 删除仓库时发生错误: {repo}")
        print(f"错误信息: {str(e)}")
        failed_repos.append(repo)

# 打印结果摘要
print("\n========== 删除操作完成 ==========")
print(f"成功删除: {deleted_count}/{len(repos)} 个仓库")

if failed_repos:
    print(f"失败: {len(failed_repos)} 个仓库")
    print("以下仓库删除失败:")
    for repo in failed_repos:
        print(f"- {repo}")
    
    # 将失败的仓库写入文件
    with open('failed_repos.txt', 'w') as f:
        for repo in failed_repos:
            f.write(f"{repo}\n")
    print("已将删除失败的仓库列表保存到 failed_repos.txt")