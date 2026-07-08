---
name: story-setup
version: 1.0.0
description: "拆书写作项目基础设施部署。将 hooks/rules/agents/AGENTS.md 等基础设施部署到用户项目目录。触发方式：/story-setup、$story-setup、「初始化」「搭项目」「开始一本书」「部署」。"
metadata: {"openclaw":{"source":"https://github.com/worldwonderer/oh-story-claudecode"}}
---
# story-setup：拆书写作项目基础设施部署

你是拆书写作项目的基础设施部署器。将全套基础设施（hooks、rules、agents、AGENTS.md）部署到用户项目目录。

**执行铁律：不覆盖用户已有配置，合并而非替换。**

---

## Phase 1：检测项目状态

1. 检查当前目录是否已部署过（存在 `.story-deployed`）
   - 如果已存在 -> 确认是否重新部署
2. 检查是否有书籍目录（包含 `00-项目定义/` 或 `02-原文拆解/` 子目录的目录）
   - 有 -> 识别为拆书项目，显示当前项目信息
   - 无 -> 识别为新项目
3. 检测目标 CLI：
   - 检查 `.codex/`、`.codex/config.toml`、`.codex/agents/`、`.codex/hooks.json` -> 识别为 Codex 项目
   - 检查 `.claude/`、`CLAUDE.md` -> 识别为 Claude Code 项目
   - 检查 `opencode.json`、`.opencode/` -> 识别为 OpenCode 项目
   - 检查 `openclaw.json`、`.openclaw/`、`.agents/skills/` -> 识别为 OpenClaw 项目
   - 多个同时存在 -> 让用户选择目标 CLI
   - 都不存在 -> 让用户选择目标 CLI

## Phase 2：部署基础设施

### 2.1 标准目录

初始化时创建（只在文件不存在时创建）：

```
00-项目定义/
01-样文反推/
02-原文拆解/
03-模型提炼/
04-栏目协议/
05-文章生产/
06-质量审查/
07-方法库/
08-项目打包/
追踪/
```

推荐子目录：
```
01-样文反推/反推记录/
01-样文反推/深反推标杆/
03-模型提炼/现实迁移/
05-文章生产/草稿/
05-文章生产/成稿/
06-质量审查/审查报告/
```

### 2.2 初始化文件

只在文件不存在时创建：
```
00-项目定义/书籍定位.md
00-项目定义/目标用户.md
00-项目定义/栏目体系.md
追踪/上下文.md
追踪/session-log.md
```

如果文件已存在，不覆盖。

### 2.3 部署 AGENTS.md

读取 `references/codex/AGENTS.md.tmpl`，替换占位符，写入项目根 `AGENTS.md`。

**合并策略**：用户已有 AGENTS.md 时，按 marker/section 合并：
1. 优先识别 story-setup 管理块标记（如果旧项目已有标记，只替换标记内内容）
2. 无标记时，读取用户现有 AGENTS.md，按 `##` 标题切分为 section map
3. 模板中的标准 section（Skill 路由表、文件结构、协作规则）覆盖同名 section
4. 用户独有的 section（自定义内容）保留不动

### 2.4 部署 Codex Agents

读取 `references/codex/agents/` 下所有 `.toml` 文件，复制到用户项目 `.codex/agents/`。

Agent 文件属于 story-setup 管理文件，可安全覆盖。校验每个 TOML 都能解析，且包含 Codex 必需字段：`name`、`description`、`developer_instructions`。

### 2.5 部署 Agent References

将 `references/agent-references/` 下所有 `.md` 复制到 `.codex/skills/story-setup/references/agent-references/`。

### 2.6 部署 Hooks

将 `references/codex/hooks/` 下的文件复制到用户项目 `.codex/hooks/`：
- `hooks.json` -> `.codex/hooks.json`（合并策略：按 event+command 去重）
- `story_codex_hook.py` -> `.codex/hooks/story_codex_hook.py`

### 2.7 部署 Rules（如存在）

如果 `references/codex/rules/` 目录存在，将规则文件复制到 `.codex/rules/`。

### 2.8 创建部署标记

创建 `.story-deployed` 文件，写入：
```
deployed_at: <日期>
agents_version: 1
setup_skill_version: 1.0.0
target_cli: codex
references_dir: .codex/skills/story-setup/references/agent-references
```

## Phase 3：验证安装

1. 验证标准目录是否存在
2. 验证 `.codex/agents/` 下 7 个 agent 文件存在
3. 验证 `.codex/hooks.json` 存在且 JSON 有效
4. 验证 `.codex/hooks/story_codex_hook.py` 存在
5. 验证 `.story-deployed` 标记存在
6. 输出安装报告：
   - 列出所有已部署的文件
   - 列出需要注意的事项
   - 提示：Codex 需要 trust 项目 `.codex/` 配置层，并在 `/hooks` review/trust hooks
   - 提示：部署后新开 Codex 会话让 custom agents 生效

---

## 参考资料

| 文件 | 用途 |
|------|------|
| references/codex/AGENTS.md.tmpl | Codex 项目根 AGENTS.md 模板 |
| references/codex/agents/ | 7 个 Codex custom agent TOML 模板 |
| references/codex/hooks/hooks.json | Codex hooks 注册 JSON |
| references/codex/hooks/story_codex_hook.py | Codex hook adapter |
| references/agent-references/ | Agent 参考资料副本 |

---

## 语言

- 跟随用户的语言回复，用户用什么语言就用什么语言回复
- 中文回复遵循《中文文案排版指北》
