# Contributing

## 如何贡献

### 报告问题

如果发现 skill 路由错误、agent 指令问题或 hooks 异常，请提交 issue 说明当前行为、预期行为和复现步骤。

### 贡献方法库

references/ 下的方法库文件欢迎补充：

1. 在对应 skill 的 references/ 目录下创建 .md 文件。
2. 文件需包含具体的方法、示例和边界说明。
3. 提交 PR 时说明该方法库的来源（样文反推、写作经验等）。

### 贡献样板项目

如果拆了新的书并跑通了完整流程，可以提交到 samples/：

1. 在 samples/ 下创建新目录。
2. 包含完整的生产流程文件（定位、反推、拆解、模型、成稿、审查）。
3. 在 README 中说明这本书的定位和栏目设计。
4. 提交前必须脱敏：删除本地绝对路径、私人资料路径、未授权竞品原文、账号信息和临时追踪日志。

## 开发指南

### 本地测试

运行静态校验：

```bash
bash scripts/static-check.sh
```

### 校验

```bash
python -B -c "import json, pathlib, tomllib; root=pathlib.Path('.'); json.load(open(root/'.codex/hooks.json')); [tomllib.loads(f.read_text()) for f in (root/'.codex/agents').glob('*.toml')]"
```

### 目录结构

.agents/skills/story*/  # skill 文件
.codex/agents/          # agent 配置
.codex/hooks/           # hooks 脚本
docs/                   # 设计文档
samples/                # 样板项目
scripts/                # 部署脚本

## 许可

本项目的工程结构基于 oh-story-claudecode 改造，遵循其开源协议。方法库内容和样板项目为独立创作。
