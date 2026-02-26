# 论文 Markdown 版本 - 发布指南

## ✅ 已完成

论文 Markdown 版本已成功生成并提交到本地 Git 仓库。

### 文件信息
- **位置**: `paper/main.md`
- **大小**: 14 KB (342 行)
- **格式**: Markdown with LaTeX math support

### 包含内容
- [x] 完整论文结构 (7个章节)
- [x] 所有表格 (4个数据表)
- [x] 算法伪代码 (2个算法)
- [x] 数学公式 (LaTeX 语法)
- [x] 引用和参考文献
- [x] 联系信息

---

## 🚀 推送到 GitHub

### 方法 1: 使用 HTTPS + Personal Access Token

```bash
cd /Users/linxiao/Downloads/clawflowgen-paper

# 1. 生成 Personal Access Token (在 GitHub 网站上)
#    Settings > Developer settings > Personal access tokens > Generate new token
#    权限需要: repo, workflow

# 2. 配置 git 使用 token
git remote set-url origin https://YOUR_TOKEN@github.com/openclawdchip/clawflowgen.git

# 3. 推送
git push origin main
```

### 方法 2: 使用 SSH 密钥

```bash
# 1. 生成 SSH 密钥 (如果还没有)
ssh-keygen -t ed25519 -C "xiao.lin@ia.ac.cn"

# 2. 添加公钥到 GitHub
#    Settings > SSH and GPG keys > New SSH key
cat ~/.ssh/id_ed25519.pub

# 3. 修改远程 URL 为 SSH
git remote set-url origin git@github.com:openclawdchip/clawflowgen.git

# 4. 推送
git push origin main
```

### 方法 3: 使用 GitHub CLI

```bash
# 1. 安装 GitHub CLI
brew install gh

# 2. 登录
gh auth login

# 3. 推送
git push origin main
```

---

## 📋 推送后检查清单

推送完成后，访问 https://github.com/openclawdchip/clawflowgen 验证：

- [ ] `paper/main.md` 文件已显示
- [ ] Markdown 渲染正常
- [ ] 数学公式正确显示
- [ ] 图片链接有效

---

## 🔗 访问链接

推送后可以通过以下链接访问：

```
https://github.com/openclawdchip/clawflowgen/blob/main/paper/main.md
```

---

## 📊 Markdown 版本特点

### 优势
1. **易于阅读**: 直接在 GitHub 上渲染，无需编译
2. **搜索友好**: 支持全文搜索
3. **移动适配**: 自动适配手机阅读
4. **链接分享**: 可直接分享特定章节

### 数学公式支持
GitHub 支持 LaTeX 数学公式：
- 行内公式: `$...$`
- 块级公式: `$$...$$`

### 表格渲染
所有表格使用 Markdown 表格语法，GitHub 会自动渲染。

---

## 📝 本地预览

推送前可以在本地预览：

```bash
# 使用 VS Code
# 安装 Markdown All in One 插件
# 按 Cmd+Shift+V 预览

# 或使用浏览器插件
# 安装 Markdown Preview 插件
```

---

**提交哈希**: `8aae4c9`  
**状态**: 已提交，待推送  
**日期**: 2026-02-26
