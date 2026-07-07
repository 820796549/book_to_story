# 拆有用书写文章生产系统 — Codex 项目说明

## 项目目标

拆有用书，写高质量文章，并让这个过程稳定复用。

竞品只用来学习写法。oh-story 只作为工程底座。

## Skill 路由表

| 命令 | Skill | 说明 |
|---|---|---|
| `$book` | book | 主入口，自动判断当前任务并路由 |
| `$book-setup` | book-setup | 初始化拆书写作项目 |
| `$book-architect` | book-architect | 书籍定位、目标用户、栏目体系 |
| `$book-reverse-style` | book-reverse-style | 竞品/样文深反推 |
| `$book-decode-source` | book-decode-source | 原文拆解、证据提取 |
| `$book-extract-model` | book-extract-model | 模型提炼、推理链整理 |
| `$book-map-application` | book-map-application | 现实迁移、认知破局映射 |
| `$book-write-column` | book-write-column | 栏目文章成稿 |
| `$book-style-polish` | book-style-polish | 表达打磨、去 AI 味 |
| `$book-review` | book-review | 质量审查、对标验收 |
| `$book-package` | book-package | 通过审查后的轻量打包 |

## 标准流程

```
书籍定位 -> 栏目设计 -> 样文反推 -> 写法库沉淀
-> 原文拆解 -> 模型提炼 -> 现实迁移
-> 单篇试写 -> 对标审查 -> 修正协议 -> 小批量生产
```

## 写正文前置条件

写栏目文章前必须存在：
- 00-项目定义/书籍定位.md
- 00-项目定义/栏目体系.md
- 04-栏目协议/对应栏目协议.md
- 01-样文反推/对应样文反推.md
- 02-原文拆解/对应篇章.md
- 03-模型提炼/对应模型.md

## 毛选样板

毛选样板位于 `samples/毛选样板/`。

第一阶段固定两个栏目：
- 底层解码篇：历史处境、当时误判、推理链、破局点
- 认知破局篇：现代痛点、错误认知、毛选模型、现实迁移、爽点句

这两个栏目不是所有书的默认栏目。换一本书必须重新做书籍定位和栏目设计。

## 协作规则

- 一次只做一个明确文件。
- 不跳过定位、反推、原文拆解直接写正文。
- 不照搬竞品表达。
- 内容质量以审查报告为准，不以生成数量为准。
