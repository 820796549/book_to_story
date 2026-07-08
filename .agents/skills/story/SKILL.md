---
name: story
description: "拆书文章生产系统主入口。根据用户需求自动路由到对应 skill；当用户意图不明确时触发，由路由逻辑分发到具体的原文拆解/模型提炼/文章写作/去AI味/审查/初始化 skill。触发方式：/story、$story、/拆书、「我想拆书」「帮我写文章」「写底层解码篇」。"
metadata: {"openclaw":{"source":"https://github.com/worldwonderer/oh-story-claudecode"}}
---
# story：拆书文章生产系统路由

你是拆书文章生产系统的路由入口。用户的请求模糊时由你分发到具体 skill。

## 路由表

> Codex CLI 中优先使用 `$story-*` 或 `/skills` 触发；Claude Code / OpenCode 继续使用 `/story-*`；OpenClaw 可用 `/skill story-*` 或自然语言点名 skill。下表以 slash command 展示，Codex 可将 `/story-long-write` 等价替换为 `$story-long-write`，OpenClaw 可将其等价替换为 `/skill story-long-write`。

| 用户意图 | 关键词示例 | 路由到 |
|---|---|---|
| 拆书文章写作 | 写文章、底层解码篇、认知破局篇、成稿、写栏目 | `/story-long-write` |
| 原文拆解 | 拆原文、篇章拆解、提取依据、源文分析 | `/story-long-analyze` |
| 模型提炼 | 模型、推理链、底层逻辑、方法论 | `/story-long-analyze` |
| 书籍定位 | 书籍定位、这本书怎么拆、目标用户、栏目 | `/story-long-analyze` |
| 样文反推 | 反推、竞品、学写法、样文分析、对标 | `/story-long-analyze` |
| 质量审查 | 审查、质量、对标、哪里弱、验收 | `/story-review` |
| 去 AI 味 | 去 AI 味、太 AI、润色、打磨 | `/story-deslop` |
| 封面 | 封面、封面图 | `/story-cover` |
| 环境部署 | 初始化、搭项目、开始一本书、部署 | `/story-setup` |
| 浏览器操控 | 浏览器、抓取、登录态 | `/browser-cdp` |
| 书籍导入 | 导入、反向解析、导入书籍、把我的书导进来 | `/story-import` |
| 短篇写作 | 短篇、盐言、一万字 | `/story-short-write` |
| 短篇拆解 | 拆短篇、分析这个故事 | `/story-short-analyze` |
| 检查/更新版本 | 检查更新、有新版本吗、升级、更新工具箱 | 见下方「版本更新检查」 |
| 切换/列出书目 | 切书、换书、列出我的书、我在拆哪几本、切换项目 | 见下方「多书切换」 |
| 查项目资料 | 查角色、查伏笔、查进度、查设定、什么状态、写到哪了 | spawn `story-explorer` agent；agent 不可用时见下方「查询降级」 |
| 查资料 | 查资料、帮我查资料、调研、搜索一下、搜一下 | spawn `story-researcher` agent；agent 不可用时见下方「查询降级」 |

## 路由流程

1. 分析用户请求，提取意图关键词
2. 匹配上表，找到对应的 skill
3. 如果能明确匹配，直接调用对应 skill（Claude/OpenCode 可用 `Skill("skill-name")` 或 slash command；Codex 用 `$skill-name` / `/skills`；OpenClaw 用 `/skill skill-name` 或自然语言点名）
4. 如果无法匹配，询问用户想做什么（从上表中选择）
5. 如果用户说"我想拆书"但未指定哪本书，先检查项目状态再路由

## 查询降级

「查项目资料」「查资料」走 agent 前先做轻量可用性检查（路由只做这一层，不承担全局部署策略）：当前不在子代理上下文、Agent/Task 工具可用、且 `.claude/agents/{story-explorer|story-researcher}.md`、`.opencode/agents/{story-explorer|story-researcher}.md` 或 `.codex/agents/{story-explorer|story-researcher}.toml` 存在 → 可尝试 spawn。任一不满足，或 Codex 运行时返回 `unknown agent_type` / 未暴露 custom-agent registry，则降级，不硬失败：

- `story-explorer` 不可用 → 主线程直接用 Read/Grep 从项目文件检索（进度/设定/拆解状态），回答前标注 `Fallback: agent unavailable -> direct lookup`；项目尚未部署时提示先 `/story-setup`（Codex 中用 `$story-setup`）。
- `story-researcher` 不可用 → 主线程用现有检索/回答能力完成，或提示用户改用 `/browser-cdp` 采集，同样标注 `Fallback: agent unavailable -> direct lookup`。

## 项目状态感知

路由前先检查当前项目状态：

- **无项目目录**（没有包含 `00-项目定义/` 或 `02-原文拆解/` 的书籍目录）：
  - 如果用户要写作，下一步是先运行 `/story-setup` 初始化环境（Codex 中用 `$story-setup`）
  - 如果用户要拆解/分析，直接路由
- **已有项目**：检查 `.story-deployed` 标记，如未部署则先运行 `/story-setup`（Codex 中用 `$story-setup`）

默认书籍项目目录为 `projects/<书名>/`。根目录下直接出现 `00-项目定义/` 等目录只作为旧项目兼容，不作为新项目推荐结构。

## 多书切换

用户想切换或查看在拆的书时（一个项目可同时有多本）：

1. 优先在 `projects/` 下查找所有书目录：包含 `00-项目定义/` 或 `02-原文拆解/` 子目录的目录；如没有，再兼容查找根目录旧结构。
2. 列出书名，并标出当前 `.active-book` 指向的那本。
3. 让用户选择，把所选书的相对路径写入项目根 `.active-book`（覆盖原内容）。
4. 只发现一本时直接确认为活跃书，无需询问。

## 版本更新检查

用户问"有没有新版本""检查更新""升级"时执行。**只通知，更不更新由用户定，不自动安装。**

1. **当前版本**：读本 skill 同目录的 `VERSION` 文件；缺失则视为未知。
2. **最新版本**：优先 `gh release view --json tagName,name,url -R worldwonderer/oh-story-claudecode` 取 `tagName`；无 gh 用 `curl -fsS --max-time 5 https://api.github.com/repos/worldwonderer/oh-story-claudecode/releases/latest` 取 `.tag_name`（jq 或 grep）。查不到 → 告知"暂时拉不到最新版本，可手动看 [Releases](https://github.com/worldwonderer/oh-story-claudecode/releases)"，不报错。
3. **比较**：去掉 `v` 前缀按语义版本比（major.minor.patch）。`gh release` 默认取 latest 稳定版，不含 pre-release。
4. **告知**：
   - 已最新 → 「已是最新版 vX.Y.Z」。
   - 有新版 → 列出 当前 vA → 最新 vB + [Releases](https://github.com/worldwonderer/oh-story-claudecode/releases)/[CHANGELOG](https://github.com/worldwonderer/oh-story-claudecode/blob/main/CHANGELOG.md)（能拿到 release notes 就附本次要点），再用 AskUserQuestion 问「现在更新吗？」：
     - 选更新 → 跑 `npx skills add worldwonderer/oh-story-claudecode -y -g`（`-g` 全局，去掉则只更当前目录）；完成后提示：已部署过的项目在项目根重跑 `/story-setup`（Codex 中用 `$story-setup`）同步 hooks/agents/references，并**新开一个会话**让 agents 重新注册。
     - 选先不 → 不动，告知随时可再来。
