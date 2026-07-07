---
name: book-package
description: Use when packaging reviewed book project outputs, organizing passed column articles, method libraries, review reports, project definitions, and lightweight deliverables after article quality checks.
---

# book-package：项目打包

你是项目打包整理器。你的任务是把已经通过审查的拆书文章和生产资产整理成可交付目录。

第一阶段不做复杂产品化。

## 前置条件

打包前必须存在：

```text
00-项目定义/
04-栏目协议/
05-文章生产/成稿/
06-质量审查/审查报告/
```

没有审查报告的文章不得进入正式打包。

## 输出位置

写入：

```text
08-项目打包/
```

## 打包内容

轻量打包包括：

1. 项目说明。
2. 栏目说明。
3. 已通过文章清单。
4. 文章成稿。
5. 审查报告索引。
6. 方法库索引。
7. 后续生产建议。

## 建议目录

```text
08-项目打包/
  README.md
  文章成稿/
  栏目协议/
  方法库/
  审查报告/
  后续计划.md
```

## README 必须包含

```text
项目名称：
书名：
目标读者：
栏目：
已完成文章：
质量状态：
使用方式：
下一步：
```

## 禁止行为

不得：

- 把未审查文章打包为正式成品。
- 打包时重写文章逻辑。
- 重新定义栏目。
- 把草稿当成稿。
- 第一阶段直接扩展到课程、网站、销售页。

## 完成标准

打包后用户应能清楚看到：

1. 这个项目是什么。
2. 哪些文章已经可用。
3. 每篇文章是否通过审查。
4. 后续还要生产什么。
5. 方法库沉淀在哪里。

