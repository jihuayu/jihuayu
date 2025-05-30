# GitHub 仓库管理脚本集

这个文件夹包含一组用于管理GitHub仓库的Python脚本，主要针对fork仓库的管理。

## 脚本列表

### find_inactive_forks.py

此脚本用于查找用户账户下超过一个月未活跃的fork仓库。

**功能**:
- 使用GitHub CLI查询用户的所有仓库
- 识别超过30天未推送更新的fork仓库
- 将这些不活跃仓库的名称保存到`repo.txt`文件中

**使用方法**:
```bash
python find_inactive_forks.py
```

**依赖**:
- 需要安装并配置GitHub CLI (gh)
- Python 3.x

### delete_repos.py

此脚本用于批量删除GitHub仓库。

**功能**:
- 读取`repo.txt`中的仓库列表
- 逐一删除这些仓库
- 生成操作结果报告，并将失败的仓库列表保存到`failed_repos.txt`

**使用方法**:
```bash
python delete_repos.py
```

**注意**:
- 删除操作不可逆，请谨慎使用！
- 执行前会要求确认

### set_repos_private.py

此脚本用于将GitHub仓库批量设置为私有。

**功能**:
- 读取`repo.txt`中的仓库列表
- 将这些仓库设置为私有
- 生成操作结果报告，并将失败的仓库列表保存到`failed_private_repos.txt`

**使用方法**:
```bash
python set_repos_private.py
```

## 使用流程

典型的使用流程是:

1. 首先运行`find_inactive_forks.py`找出不活跃的fork仓库
2. 查看生成的`repo.txt`，确认要处理的仓库列表
3. 根据需要，运行`delete_repos.py`删除这些仓库，或者运行`set_repos_private.py`将它们设置为私有

## 注意事项

- 所有脚本都依赖于GitHub CLI，请确保已正确安装和配置
- 这些操作可能受到GitHub API速率限制的影响
- 删除操作不可逆，请在操作前备份重要数据
