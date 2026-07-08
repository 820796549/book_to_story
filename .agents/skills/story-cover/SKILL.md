---
name: story-cover
version: 1.0.0
description: "拆书文章封面生成。根据书名、栏目类型自动分析题材风格，生成封面图片。触发方式：/story-cover、$story-cover、「封面」「封面图」。"
metadata: {"openclaw":{"source":"https://github.com/worldwonderer/oh-story-claudecode"}}
---
# story-cover：拆书文章封面生成

根据书名、栏目类型自动分析题材风格，生成封面图片。

---

## 流程

1. 读取当前项目 `00-项目定义/书籍定位.md`，获取书名和定位
2. 分析栏目类型（底层解码篇/认知破局篇/其他）
3. 根据栏目类型确定封面风格
4. 调用图片生成能力生成封面
5. 保存到 `05-文章生产/成稿/` 对应目录

---

## 参考资料

| 场景 | 加载文件 |
|------|---------|
| 封面风格 | `references/cover-styles.md` |

---

## 语言

- 跟随用户的语言回复
- 中文回复遵循《中文文案排版指北》
