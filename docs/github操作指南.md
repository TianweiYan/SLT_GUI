# Git与GitHub完整操作指南：上传Python工程

## 📋 目录
- [前期准备](#前期准备)
- [本地Git初始化](#本地git初始化)
- [配置GitHub仓库](#配置github仓库)
- [推送到GitHub](#推送到github)
- [日常维护操作](#日常维护操作)
- [最佳实践](#最佳实践)
- [故障排除](#故障排除)

## 🚀 前期准备

### 1.1 软件安装确认
- ✅ [Git](https://git-scm.com/downloads) - 已安装
- ✅ [GitHub账号](https://github.com) - 已创建

### 1.2 Git基础配置（如果未配置）
```bash
# 设置全局用户名和邮箱（与GitHub一致）
git config --global user.name "YourGitHubUsername"
git config --global user.email "your-email@example.com"

# 可选：设置默认分支名称为main
git config --global init.defaultBranch main

# 验证配置
git config --list
```

## 📁 本地Git初始化

### 2.1 进入项目目录并初始化
```bash
# 导航到你的Python项目文件夹
cd /path/to/your/python-project

# 初始化Git仓库
git init
```

### 2.2 创建.gitignore文件（重要！）
在项目根目录创建`.gitignore`文件，防止敏感文件和不必要文件被上传：

```gitignore
# Python特定文件
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
ENV/
env.bak/
venv.bak/
pip-selfcheck.json

# 包和依赖
*.egg
*.egg-info/
dist/
build/
eggs/
parts/
var/
sdist/
develop-eggs/
.installed.cfg
lib/
lib64/

# 安装包日志
pip-log.txt
pip-delete-this-directory.txt

# 单元测试/覆盖率
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Jupyter笔记本
.ipynb_checkpoints

# IDE配置文件
.vscode/
.idea/
*.swp
*.swo
*~

# 操作系统文件
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# 日志和数据库
*.log
*.sql
*.sqlite3
*.db

# 环境变量文件
.env
.secret
```

### 2.3 检查项目状态
```bash
# 查看哪些文件会被追踪
git status
```

### 2.4 添加文件到暂存区
```bash
# 方法1：添加所有文件（除了.gitignore指定的）
git add .

# 方法2：逐个添加特定文件
git add main.py utils.py README.md requirements.txt
```

### 2.5 提交更改
```bash
# 提交到本地仓库
git commit -m "Initial commit: Python project setup"

# 查看提交历史
git log --oneline
```

## 🌐 配置GitHub仓库

### 3.1 创建GitHub仓库
1. 登录 [GitHub](https://github.com)
2. 点击右上角 **+** → **New repository**
3. 填写仓库信息：
   - **Repository name**: 项目名称（如：my-python-app）
   - **Description**: 项目描述（可选）
   - **Public/Private**: 选择可见性
   - **☐ Initialize with README**: **不要勾选**（已有本地仓库）
   - **☐ Add .gitignore**: **不要勾选**（已有）
   - **☐ Choose a license**: 可选
4. 点击 **Create repository**

### 3.2 连接本地与远程仓库
创建成功后，复制仓库的HTTPS或SSH URL，然后执行：

```bash
# 添加远程仓库（替换为你的URL）
git remote add origin https://github.com/yourusername/your-repo-name.git

# 验证远程仓库设置
git remote -v
# 应该显示：
# origin  https://github.com/yourusername/your-repo-name.git (fetch)
# origin  https://github.com/yourusername/your-repo-name.git (push)
```

## ⬆️ 推送到GitHub

### 4.1 首次推送
```bash
# 重命名主分支为main（如果需要）
git branch -M main

# 推送到GitHub并设置上游分支
git push -u origin main

# -u参数设置上游分支，以后只需git push即可
```

### 4.2 身份验证
如果提示输入凭据：
- **用户名**: 你的GitHub用户名
- **密码**: 使用**个人访问令牌**（不是GitHub密码）
  - 创建令牌：GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
  - 权限：勾选 `repo`（完全控制仓库）

## 🔄 日常维护操作

### 5.1 基本工作流程
```bash
# 1. 查看状态
git status

# 2. 查看具体修改内容
git diff

# 3. 添加修改的文件
git add <file1> <file2>
# 或
git add .

# 4. 提交更改
git commit -m "描述本次修改：修复了XX功能，添加了XX特性"

# 5. 推送到GitHub
git push
```

### 5.2 查看提交历史
```bash
# 简洁查看
git log --oneline

# 图形化查看
git log --oneline --graph --all

# 查看最近5次提交
git log -5 --oneline
```

### 5.3 忽略已提交的文件
如果意外提交了不该提交的文件：
```bash
# 1. 从Git中移除但保留本地文件
git rm --cached <file>

# 2. 更新.gitignore
echo "<file>" >> .gitignore

# 3. 提交更改
git add .gitignore
git commit -m "Remove <file> from tracking"
git push
```

## 🏆 最佳实践

### 6.1 创建项目文档

**README.md 模板：**
```markdown
# 项目名称

## 项目简介
简要描述项目功能、用途和特点

## 🚀 快速开始

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行项目
```bash
python main.py
```

## 📁 项目结构
```
project/
├── src/           # 源代码目录
│   ├── __init__.py
│   ├── main.py
│   └── utils.py
├── tests/         # 测试文件
├── data/          # 数据文件
├── docs/          # 文档
├── requirements.txt
├── README.md
└── .gitignore
```

## 📝 功能特性
- 功能1
- 功能2
- 功能3

## 🛠 技术栈
- Python 3.x
- 相关库1
- 相关库2

## 📄 许可证
MIT License
```

**requirements.txt 生成：**
```bash
# 导出当前环境依赖
pip freeze > requirements.txt

# 安装依赖
pip install -r requirements.txt
```

### 6.2 推荐的项目结构
```
my-python-project/
├── .gitignore
├── README.md
├── requirements.txt
├── setup.py           # 可选，用于打包
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   ├── utils/
│   └── config.py
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── conftest.py
├── data/
│   └── sample.csv
├── docs/
│   ├── api.md
│   └── user_guide.md
└── .github/
    └── workflows/     # GitHub Actions
```

### 6.3 提交信息规范
使用有意义的提交信息：
- ✨ 新功能：`git commit -m "feat: add user authentication system"`
- 🐛 修复bug：`git commit -m "fix: resolve login timeout issue"`
- 📝 文档更新：`git commit -m "docs: update API documentation"`
- ♻️ 代码重构：`git commit -m "refactor: simplify database connection"`
- 🚀 性能优化：`git commit -m "perf: optimize image loading speed"`

## 🔧 故障排除

### 7.1 常见问题

**问题1：推送被拒绝**
```bash
# 先拉取远程更改
git pull origin main

# 如果有冲突，解决冲突后
git add .
git commit -m "Resolve merge conflicts"
git push
```

**问题2：忘记添加某些文件**
```bash
# 添加遗漏的文件
git add missing_file.py

# 合并到上一个提交
git commit --amend --no-edit
git push -f  # 谨慎使用，会重写历史
```

**问题3：误提交大文件**
```bash
# 从Git历史中移除大文件
git filter-branch --tree-filter 'rm -f large_file.zip' HEAD
git push -f origin main
```

### 7.2 Git命令速查表
```bash
# 基础命令
git init                    # 初始化仓库
git clone <url>             # 克隆远程仓库
git add <file>              # 添加到暂存区
git commit -m "message"     # 提交更改
git push                    # 推送到远程
git pull                    # 拉取远程更改

# 分支管理
git branch                  # 查看分支
git branch <name>           # 创建分支
git checkout <branch>       # 切换分支
git merge <branch>          # 合并分支

# 撤销操作
git restore <file>          # 丢弃工作区修改
git reset HEAD <file>       # 取消暂存
git checkout -- <file>      # 恢复文件

# 远程操作
git remote add <name> <url> # 添加远程仓库
git remote -v               # 查看远程仓库
git fetch                   # 获取远程更新
```

## 📚 高级配置（可选）

### 8.1 使用SSH密钥（推荐）
```bash
# 1. 生成SSH密钥
ssh-keygen -t ed25519 -C "your-email@example.com"

# 2. 复制公钥
cat ~/.ssh/id_ed25519.pub

# 3. 添加到GitHub
# Settings → SSH and GPG keys → New SSH key

# 4. 测试连接
ssh -T git@github.com

# 5. 修改远程URL为SSH
git remote set-url origin git@github.com:username/repo.git
```

### 8.2 Git别名设置
```bash
# 添加到 ~/.gitconfig
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    lg = log --oneline --graph --all
    last = log -1 HEAD
    unstage = reset HEAD --
```

---

## 💡 总结流程
1. **本地准备**：初始化Git、配置.gitignore
2. **首次提交**：添加文件并提交到本地仓库
3. **GitHub创建**：在GitHub创建空仓库
4. **建立连接**：添加远程仓库URL
5. **推送代码**：推送到GitHub
6. **日常维护**：按照工作流程更新代码

🎉 恭喜！现在你的Python项目已成功托管在GitHub上，可以进行版本控制和协作开发了。