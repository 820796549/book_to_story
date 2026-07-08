---
name: story-import
version: 1.0.0
description: "逆向导入已有书籍。将已写好的书籍（半成品或完本）反向解析为标准项目目录结构，包括原文、拆解、模型等。触发方式：/story-import、$story-import、「导入」「反向解析」「导入书籍」。"
metadata: {"openclaw":{"source":"https://github.com/worldwonderer/oh-story-claudecode"}}
---
# story-import：书籍导入

将已写好的书籍或原文（半成品或完本）反向解析为标准项目目录结构。

---

## 流程

1. 读取用户提供的书籍文件或目录
2. 分析书籍结构（篇章、章节）
3. 创建标准目录结构
4. 将原文复制到 `原文/` 目录
5. 生成初始项目定义文件
6. 提示下一步操作

---

## 参考资料

| 场景 | 加载文件 |
|------|---------|
| 格式与结构 | `references/format-and-structure.md` |
| 状态追踪 | `references/state-tracking.md` |
| 长篇结构映射 | `references/structure-mapping-long.md` |
| 短篇结构映射 | `references/structure-mapping-short.md` |

---

## 语言

- 跟随用户的语言回复
- 中文回复遵循《中文文案排版指北》
