# GitHub 发布指南

## 📋 发布准备

### 1. 创建 GitHub 组织

1. 访问 https://github.com/organizations/plan
2. 创建新组织: **openclawdchip**
3. 选择免费计划 (Free)

### 2. 创建仓库

在 openclawdchip 组织下创建新仓库:
- **仓库名**: clawflowgen
- **描述**: Physically-Parallel Evolutionary Processor Generator
- **可见性**: Public
- **初始化**: 不初始化 (我们将推送现有代码)

### 3. 初始化并推送代码

```bash
# 进入项目目录
cd /Users/linxiao/Downloads/clawflowgen-paper/github

# 初始化 git 仓库 (如果尚未初始化)
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: ClawFlowGen v0.1.0

- Four-stage evolutionary processor generation
- Support for CPU and NPU targets
- Automatic interconnect generation
- Complete test suite and examples
- Academic paper and documentation"

# 添加远程仓库
git remote add origin https://github.com/openclawdchip/clawflowgen.git

# 推送
git push -u origin main
```

### 4. 配置仓库设置

在 GitHub 仓库页面:

1. **Settings > General**
   - 启用 Issues
   - 启用 Discussions
   - 启用 Projects

2. **Settings > Branches**
   - 添加分支保护规则
   - 要求 PR 审查
   - 要求状态检查通过

3. **Settings > Secrets and variables > Actions**
   - 添加 PYPI_API_TOKEN (用于发布到 PyPI)

### 5. 创建 Release

```bash
# 创建标签
git tag -a v0.1.0 -m "Release v0.1.0: Initial release"

# 推送标签
git push origin v0.1.0
```

GitHub Actions 将自动创建 Release 并构建发布包。

## 📦 发布到 PyPI

### 1. 注册 PyPI 账户

访问 https://pypi.org/ 并注册账户

### 2. 创建 API Token

在 PyPI 账户设置中创建 API Token

### 3. 添加到 GitHub Secrets

在仓库设置中添加 Secret: `PYPI_API_TOKEN`

### 4. 手动发布 (可选)

```bash
# 安装构建工具
pip install build twine

# 构建
python -m build

# 检查
twine check dist/*

# 上传
 twine upload dist/*
```

## 🎨 设置 GitHub Pages

### 1. 启用 Pages

Settings > Pages > Source: Deploy from a branch > Branch: main /docs folder

### 2. 配置文档

确保 docs/ 目录包含 index.html 或使用静态站点生成器

## 📊 发布后检查清单

- [ ] 仓库已成功创建在 openclawdchip 组织下
- [ ] 代码已推送到 main 分支
- [ ] README 正确显示
- [ ] GitHub Actions CI 正常工作
- [ ] v0.1.0 Release 已创建
- [ ] PyPI 包已发布
- [ ] GitHub Pages 已启用
- [ ] 贡献指南链接有效

## 🔗 重要链接

- 组织: https://github.com/openclawdchip
- 仓库: https://github.com/openclawdchip/clawflowgen
- 联系: xiao.lin@ia.ac.cn
- 文档: https://docs.clawflowgen.ai (待配置)

## 🆘 常见问题

### 1. 推送被拒绝

```bash
# 强制推送 (谨慎使用)
git push -f origin main
```

### 2. GitHub Actions 失败

检查:
- Python 版本兼容性
- 依赖项是否正确安装
- 测试是否通过

### 3. PyPI 上传失败

确保:
- API Token 正确添加到 Secrets
- 包名在 PyPI 上唯一
- 版本号遵循语义化版本

## 📞 联系支持

如有问题，请联系: **xiao.lin@ia.ac.cn**
