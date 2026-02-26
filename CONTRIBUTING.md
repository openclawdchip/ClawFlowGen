# 贡献指南

感谢您对 ClawFlowGen 项目的关注！我们欢迎所有形式的贡献，包括但不限于：

- 报告 Bug
- 提交功能请求
- 改进文档
- 提交代码修复
- 分享使用案例

## 如何贡献

### 1. 报告问题

如果您发现了 Bug 或有功能建议，请通过 [GitHub Issues](https://github.com/openclawdchip/clawflowgen/issues) 提交。

提交问题时，请包含以下信息：
- 问题的清晰描述
- 重现步骤（如果适用）
- 期望的行为
- 实际的行为
- 环境信息（操作系统、Python 版本等）

### 2. 提交代码

#### 准备工作

1. Fork 本仓库
2. 克隆您的 Fork 到本地
```bash
git clone https://github.com/yourusername/clawflowgen.git
cd clawflowgen
```

3. 创建新的分支
```bash
git checkout -b feature/your-feature-name
```

#### 开发规范

- **代码风格**: 我们使用 Black 进行代码格式化
```bash
black src/ tests/
```

- **类型注解**: 所有函数都应包含类型注解
- **文档字符串**: 所有公共函数都应包含 docstring
- **测试**: 新功能必须包含单元测试

#### 提交代码

1. 添加您的更改
```bash
git add .
```

2. 提交更改（使用清晰的提交信息）
```bash
git commit -m "feat: add new operator type support"
```

提交信息格式：
- `feat:` 新功能
- `fix:` 修复 Bug
- `docs:` 文档更新
- `test:` 测试相关
- `refactor:` 代码重构
- `style:` 代码格式

3. 推送到您的 Fork
```bash
git push origin feature/your-feature-name
```

4. 创建 Pull Request

### 3. 代码审查

所有提交都需要通过代码审查。维护者会检查：
- 代码质量
- 测试覆盖率
- 文档完整性
- 是否符合项目风格

## 开发环境设置

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
pytest

# 检查代码风格
flake8 src/
black --check src/
```

## 项目结构

```
clawflowgen/
├── src/               # 源代码
├── tests/             # 测试代码
├── docs/              # 文档
├── examples/          # 示例
└── paper/             # 学术论文
```

## 行为准则

参与本项目即表示您同意遵守我们的 [行为准则](CODE_OF_CONDUCT.md)。

## 联系方式

如有任何问题，请联系：
- 邮箱: xiao.lin@ia.ac.cn
- GitHub Discussions

感谢您的贡献！
