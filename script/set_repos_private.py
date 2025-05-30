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
    print("repo.txt 中没有仓库名称，无需执行操作。")
    sys.exit(0)

# 确认操作
print(f"将要设置以下 {len(repos)} 个仓库为私有:")
for repo in repos:
    print(f"- {repo}")
confirmation = input("\n请输入 'yes' 确认将这些仓库设置为私有: ")

if confirmation.lower() != 'yes':
    print("操作已取消。")
    sys.exit(0)

# 开始设置仓库为私有
success_count = 0
failed_repos = []

for repo in repos:
    print(f"\n正在将仓库设置为私有: {repo}")
    try:
        # 使用gh命令设置仓库为私有，添加必要的接受后果标志
        result = subprocess.run(
            ['gh', 'repo', 'edit', repo, '--visibility', 'private', '--accept-visibility-change-consequences'],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            print(f"✅ 成功将仓库设置为私有: {repo}")
            success_count += 1
        else:
            print(f"❌ 设置仓库为私有失败: {repo}")
            print(f"错误信息: {result.stderr}")
            failed_repos.append(repo)

        # 添加短暂延迟避免触发GitHub API限制
        time.sleep(1)

    except Exception as e:
        print(f"❌ 设置仓库为私有时发生错误: {repo}")
        print(f"错误信息: {str(e)}")
        failed_repos.append(repo)

# 打印结果摘要
print("\n========== 操作完成 ==========")
print(f"成功设置: {success_count}/{len(repos)} 个仓库为私有")

if failed_repos:
    print(f"失败: {len(failed_repos)} 个仓库")
    print("以下仓库设置失败:")
    for repo in failed_repos:
        print(f"- {repo}")

    # 将失败的仓库写入文件
    with open('failed_private_repos.txt', 'w') as f:
        for repo in failed_repos:
            f.write(f"{repo}\n")
    print("已将设置失败的仓库列表保存到 failed_private_repos.txt")