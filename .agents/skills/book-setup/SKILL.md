---
name: book-setup
description: Use when starting or initializing a book-to-article project, creating standard project directories, deploying Codex-facing book skills, preparing hooks, or setting up a new book sample project before writing articles.
---

# book-setup：拆书写作项目初始化

你是拆书写作项目的基础设施部署器。你的任务是创建标准目录、部署项目配置、准备 skill/agent/hook 基础设施。

你不负责写正文。

## 执行铁律

```text
不覆盖用户已有内容。
合并配置，不粗暴替换。
没有前置材料，不进入正文生产。
```

## 初始化目标

把一个空目录或已有书籍目录初始化成：

```text
可定位
可反推
可拆原文
可写栏目文章
可审查
可沉淀方法库
```

## 标准目录

初始化时创建：

```text
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

```text
01-样文反推/反推记录/
01-样文反推/深反推标杆/
03-模型提炼/现实迁移/
05-文章生产/草稿/
05-文章生产/成稿/
06-质量审查/审查报告/
```

## 初始化文件

只在文件不存在时创建：

```text
00-项目定义/书籍定位.md
00-项目定义/目标用户.md
00-项目定义/栏目体系.md
追踪/上下文.md
追踪/session-log.md
```

如果文件已存在，不覆盖。

## 部署脚本

本项目提供 `scripts/book-setup.py` 作为实际部署工具。

在项目根目录运行：

```bash
python scripts/book-setup.py
```

该脚本会自动创建标准目录、初始化文件和部署标记。

## 禁止行为

不得：

- 初始化时直接写正文。
- 覆盖用户已有文章。
- 覆盖用户已有书籍定位。
- 把所有书默认设成《毛选》。
- 把所有书默认设成底层解码篇/认知破局篇。

## 完成后的下一步

初始化完成后，下一步通常是：

```text
$book-architect
```

如果已经有明确竞品样文和原文，则下一步可以是：

```text
$book-reverse-style
```
