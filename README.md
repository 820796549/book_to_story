# 拆有用书写文章生产系统

## 定位

```text
拆有用书，写高质量文章，并让这个过程稳定复用。
```

竞品只用来学习写法。oh-story 只作为工程底座。

## 目录结构

```
.agents/skills/book*/   # book 系列 skill（11 个）
.codex/agents/          # Codex custom agents（7 个）
.codex/hooks.json       # Codex hooks 配置
.codex/hooks/           # Codex hooks 脚本
docs/                   # 设计文档
samples/                # 样板项目
scripts/                # 部署脚本
AGENTS.md               # Codex 项目说明
```

## Codex 使用方式

在本项目根目录新开 Codex 会话后，可以使用：

```
$book              # 主入口，自动路由
$book-setup        # 初始化拆书项目
$book-architect    # 书籍定位与栏目设计
$book-reverse-style # 样文深反推
$book-decode-source # 原文拆解
$book-extract-model # 模型提炼
$book-map-application # 现实迁移
$book-write-column  # 栏目文章成稿
$book-style-polish  # 表达打磨
$book-review        # 质量审查
$book-package       # 项目打包
```

## 推荐流程

```
$book-setup -> $book-architect -> $book-reverse-style
-> $book-decode-source -> $book-extract-model
-> $book-map-application -> $book-write-column -> $book-review
```

## 样板项目

毛选样板位于 `samples/毛选样板/`。

## Codex 配置

新开 Codex 会话后，需要：

1. 信任当前项目 .codex 配置层
2. 在 /hooks 中 review/trust hooks
3. 再次新开或刷新 Codex 会话，让 custom agents 生效
