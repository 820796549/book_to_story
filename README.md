# 拆有用书写文章生产系统模板

## 定位

```text
拆有用书，写高质量文章，并让这个过程稳定复用。
```

竞品只用来学习写法。oh-story 只作为工程底座。

这个仓库是系统模板，不是某一本书的生产项目。用户自己的书籍定位、原文拆解、模型提炼、成稿和审查报告应留在本地工作区，不建议提交到模板仓库。

## 目录结构

```
.agents/skills/story*/  # 拆书写作 skill
.agents/skills/browser-cdp/ # 浏览器采集辅助
.codex/agents/          # Codex custom agents
.codex/hooks.json       # Codex hooks 配置
.codex/hooks/           # Codex hooks 脚本
docs/                   # 设计文档
samples/                # 脱敏样板项目
scripts/                # 部署脚本
AGENTS.md               # Codex 项目说明
```

## Codex 使用方式

在本项目根目录新开 Codex 会话后，可以使用：

```
$story              # 主入口，自动路由
$story-setup        # 初始化拆书写作项目
$story-long-analyze # 书籍定位、样文反推、原文拆解、模型提炼
$story-long-write   # 栏目文章成稿
$story-review       # 质量审查、对标验收
$story-deslop       # 表达打磨、去 AI 味
$story-cover        # 封面生成
$story-import       # 书籍导入、反向解析
$browser-cdp        # 浏览器操控、资料采集
```

## 推荐流程

```
$story-setup -> $story-long-analyze -> $story-long-write
-> $story-review -> $story-deslop
```

标准生产顺序：

```
书籍定位 -> 栏目设计 -> 样文反推 -> 原文拆解
-> 模型提炼 -> 现实迁移 -> 单篇试写
-> 对标审查 -> 表达打磨 -> 小批量生产
```

## 样板项目

脱敏样板位于 `samples/毛选样板/`，用于展示目录结构和流程形态。样板中的本地路径已替换为占位路径，真实生产时请改成自己的原文和样文位置。

## 本地工作区

以下目录默认被 `.gitignore` 排除，适合放用户自己的生产材料：

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
参考资料/
追踪/
```

## Codex 配置

新开 Codex 会话后，需要：

1. 信任当前项目 .codex 配置层
2. 在 /hooks 中 review/trust hooks
3. 再次新开或刷新 Codex 会话，让 custom agents 生效
