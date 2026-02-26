# ClawFlowGen GitHub 仓库结构

## 📂 当前目录结构 (已配置为 GitHub 仓库)

```
/Users/linxiao/Downloads/clawflowgen-paper/    ← GitHub 仓库根目录
│
├── 核心项目文件
│   ├── README.md                    # 项目主页 (带封面图)
│   ├── LICENSE                      # MIT 许可证
│   ├── CONTRIBUTING.md              # 贡献指南
│   ├── CODE_OF_CONDUCT.md           # 行为准则
│   ├── .gitignore                   # Git 忽略配置
│   ├── setup.py                     # Python 包配置
│   └── pyproject.toml               # 现代 Python 项目配置
│
├── 依赖配置
│   ├── requirements.txt             # 运行依赖
│   └── requirements-dev.txt         # 开发依赖
│
├── Python 源代码 (src/clawflowgen/)
│   ├── __init__.py                  # 包初始化
│   ├── core.py                      # 核心生成器 (ProcessorGenerator)
│   ├── operators.py                 # 算子库
│   ├── interconnect.py              # 互联模块 (Crossbar/Mesh/NoC)
│   ├── memory.py                    # 内存模块 (RegFile/Cache/LSU)
│   └── cli.py                       # 命令行接口
│
├── 测试 (tests/)
│   ├── __init__.py
│   └── test_core.py                 # 单元测试
│
├── 示例 (examples/)
│   ├── generate_cpu.py              # CPU 生成示例
│   └── generate_npu.py              # NPU 生成示例
│
├── 文档 (docs/)
│   └── index.md                     # 文档首页
│
├── CI/CD (.github/workflows/)
│   ├── ci.yml                       # 持续集成 (测试/代码检查)
│   └── release.yml                  # 自动发布
│
├── 静态资源 (assets/)
│   └── hero_image.png               # 项目封面图 (1.7MB)
│
├── 根目录文件
│   └── index.html                   # 🌐 交互式论文演示 (HTML)
│
├── 学术论文 (paper/)
│   ├── main.tex                     # 完整学术论文 (LaTeX)
│   ├── main.md                      # Markdown 版本 (在线阅读)
│   ├── figures/
│   │   ├── clawflowgen_concept.png  # 概念插图
│   │   ├── fig1_evolution.tex       # TikZ 图1: 四阶段演化
│   │   ├── fig2_parallelism.tex     # TikZ 图2: 并行对比
│   │   └── fig3_architecture.tex    # TikZ 图3: 架构对比
│   └── supplementary/
│       └── supplementary.tex        # 详细补充材料
│
├── 博客文章 (blog/)
│   └── technical-blog.md            # 技术博客
│
├── 新闻稿 (news/)
│   └── press-release.md             # 新闻发布稿
│
└── 项目文档
    ├── PROJECT_REPORT.md            # 项目完成报告
    └── GITHUB_RELEASE_GUIDE.md      # GitHub 发布指南
```

## 📊 文件统计

| 类别 | 文件数 | 说明 |
|------|--------|------|
| 核心代码 | 6 | Python 源文件 |
| 测试 | 2 | 单元测试 |
| 示例 | 2 | CPU/NPU 示例 |
| CI/CD | 2 | GitHub Actions |
| 文档 | 8 | README/CONTRIBUTING等 |
| 论文 | 7 | LaTeX + Markdown + 图片 |
| 交互式演示 | 1 | HTML (Tailwind CSS + Chart.js) |
| 博客/新闻 | 2 | 发布内容 |
| **总计** | **~36** | **3.7 MB** |

## 🏢 发布信息

- **组织**: [openclawdchip](https://github.com/openclawdchip)
- **仓库**: https://github.com/openclawdchip/clawflowgen
- **联系邮箱**: xiao.lin@ia.ac.cn
- **许可证**: MIT

## 🚀 快速发布

```bash
cd /Users/linxiao/Downloads/clawflowgen-paper

# 1. 初始化 Git
git init

# 2. 添加所有文件
git add .

# 3. 提交
git commit -m "Initial commit: ClawFlowGen v0.1.0

- Four-stage evolutionary processor generation
- Support for CPU (8-issue OoO) and NPU (256-PE Systolic)
- Automatic interconnect generation (Crossbar/Mesh/NoC)
- Complete test suite with pytest
- CLI interface for easy usage
- Academic paper with experimental validation
- CI/CD with GitHub Actions"

# 4. 添加远程仓库
git remote add origin https://github.com/openclawdchip/clawflowgen.git

# 5. 推送
git push -u origin main

# 6. 创建标签 (触发 Release)
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

## ✅ 发布前检查清单

- [x] README.md 包含组织信息和联系方式
- [x] LICENSE 为 MIT 许可证
- [x] setup.py 和 pyproject.toml 已配置
- [x] CI/CD 工作流已配置
- [x] 单元测试已编写
- [x] 示例代码已提供
- [x] 学术论文完整 (main.tex + main.md + supplementary.tex)
- [x] 插图已包含 (TikZ 源码 + AI 概念图)
- [x] 技术博客和新闻稿已准备
- [x] 贡献指南和行为准则已添加
- [x] **交互式 HTML 演示 (index.html)** 已添加
- [x] GitHub Pages 配置就绪

## 📚 包含的内容

### 1. Python 包 (clawflowgen)
- 核心生成器: `ProcessorGenerator`
- 四阶段演化算法实现
- 支持 CPU (乱序调度) 和 NPU (脉动阵列)
- 命令行接口: `clawflowgen --target CPU --parallelism 8`

### 2. 学术论文
- 18KB LaTeX 源码 (main.tex)
- 14KB Markdown 版本 (main.md)
- 3张 TikZ 矢量图
- 详细补充材料 (11KB)
- 完整实验数据表格

### 3. 交互式演示
- **index.html** - 交互式论文展示
- 三阶段演化可视化
- 实时性能图表 (Chart.js)
- 仲裁算法交互演示
- 响应式设计

### 4. 发布内容
- 技术博客 (适合 Medium/知乎)
- 新闻稿 (适合 TechCrunch/36氪)
- GitHub 发布指南

## 🎉 准备就绪！

当前目录 `/Users/linxiao/Downloads/clawflowgen-paper/` 已配置为完整的 GitHub 仓库，可以直接推送！
