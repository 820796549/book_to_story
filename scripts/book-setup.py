#!/usr/bin/env python3
"""book-setup: 拆书写作项目初始化部署脚本"""

import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path


def project_root() -> Path:
    env = os.environ.get("CODEX_PROJECT_DIR") or os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        return Path(env).resolve()
    return Path.cwd().resolve()


def find_skill_root(root: Path) -> Path | None:
    """Find the book-setup skill directory."""
    candidates = [
        root / ".agents" / "skills" / "book-setup",
        root / ".codex" / "skills" / "book-setup",
        root / "skills" / "book-setup",
    ]
    for c in candidates:
        if c.is_dir():
            return c
    return None


def ensure_dirs(root: Path):
    dirs = [
        "00-项目定义",
        "01-样文反推/反推记录",
        "01-样文反推/深反推标杆",
        "02-原文拆解",
        "03-模型提炼/现实迁移",
        "04-栏目协议",
        "05-文章生产/草稿",
        "05-文章生产/成稿",
        "06-质量审查/审查报告",
        "07-方法库",
        "08-项目打包",
        "追踪",
    ]
    for d in dirs:
        (root / d).mkdir(parents=True, exist_ok=True)
    print(f"[book-setup] 已创建 {len(dirs)} 个目录")


def ensure_init_files(root: Path):
    files = {
        "00-项目定义/书籍定位.md": "# 书籍定位\n\n## 基本信息\n\n- 书名：\n- 作者：\n- 原文类型：\n- 拆解范围：\n\n## 一句话定位\n\n```text\n把《书名》从 [原始形态]，\n转成 [目标读者] 能用于 [核心场景] 的 [知识产品形态]。\n```\n",
        "00-项目定义/目标用户.md": "# 目标用户\n\n## 用户处境\n\n当用户处于 [具体处境]，\n他想通过这本书获得 [理解/判断/行动/表达/陪伴]，\n从而完成 [具体结果]。\n",
        "00-项目定义/栏目体系.md": "# 栏目体系\n\n## 栏目列表\n\n| 栏目名称 | 栏目目的 | 第一阶段启用 |\n|---|---|---|\n",
        "追踪/上下文.md": "# 上下文快照\n\n- 更新时间：\n- 当前书籍：\n- 当前阶段：\n",
        "追踪/session-log.md": "# 会话日志\n\n| 时间 | 完成内容 | 修改文件 | 当前阶段 |\n|---|---|---|---|\n",
    }
    created = 0
    for rel, content in files.items():
        path = root / rel
        if not path.exists():
            path.write_text(content, encoding="utf-8")
            created += 1
    print(f"[book-setup] 已创建 {created} 个初始化文件（跳过已有文件）")


def deploy_templates(root: Path, skill_root: Path):
    """Deploy templates to target project."""
    template_dir = skill_root / "references" / "templates"
    if not template_dir.is_dir():
        print("[book-setup] 未找到模板目录，跳过模板部署")
        return

    # Deploy CLAUDE.md
    tmpl = template_dir / "CLAUDE.md.tmpl"
    if tmpl.exists():
        target = root / "CLAUDE.md"
        if not target.exists():
            content = tmpl.read_text(encoding="utf-8")
            content = content.replace("{{BOOK_NAME}}", root.name)
            content = content.replace("{{BOOK_DESCRIPTION}}", "拆有用书写文章生产系统")
            target.write_text(content, encoding="utf-8")
            print(f"[book-setup] 已创建 CLAUDE.md")

    # Deploy hooks.json
    hooks_tmpl = template_dir / "settings-hooks.json"
    if hooks_tmpl.exists():
        target = root / ".codex" / "hooks.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            shutil.copy2(str(hooks_tmpl), str(target))
            print(f"[book-setup] 已部署 hooks.json")

    # Deploy context template
    ctx_tmpl = template_dir / "上下文.md.tmpl"
    if ctx_tmpl.exists():
        target = root / "追踪" / "上下文.md"
        if not target.exists():
            content = ctx_tmpl.read_text(encoding="utf-8")
            content = content.replace("{{BOOK_NAME}}", root.name)
            content = content.replace("{{UPDATE_TIME}}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            content = content.replace("{{CURRENT_PHASE}}", "初始化")
            content = content.replace("{{COMPLETED_FILES}}", "- 项目初始化")
            target.write_text(content, encoding="utf-8")
            print(f"[book-setup] 已创建 追踪/上下文.md")


def write_sentinel(root: Path):
    sentinel = root / ".book-deployed"
    content = (
        "system=book-to-article\n"
        "target_cli=codex\n"
        f"deployed_at={datetime.now().strftime('%Y-%m-%d')}\n"
        "status=initialized\n"
        "entry_skill=book\n"
    )
    sentinel.write_text(content, encoding="utf-8")
    print(f"[book-setup] 已写入部署标记")


def main():
    root = project_root()
    print(f"[book-setup] 项目根目录: {root}")

    skill_root = find_skill_root(root)
    if not skill_root:
        print("[book-setup] 未找到 book-setup skill 目录，尝试从系统 skill 目录查找")
        # Try common system skill paths
        for p in [
            Path(os.environ.get("CODEX_HOME", "")) / "skills" / "book-setup",
            Path.home() / ".codex" / "skills" / "book-setup",
            Path.home() / ".agents" / "skills" / "book-setup",
        ]:
            if p.is_dir():
                skill_root = p
                break

    ensure_dirs(root)
    ensure_init_files(root)

    if skill_root:
        deploy_templates(root, skill_root)
    else:
        print("[book-setup] 未找到 skill 目录，跳过模板部署")

    write_sentinel(root)

    print()
    print("[book-setup] 初始化完成。下一步建议:")
    print("  1. 填写 00-项目定义/书籍定位.md")
    print("  2. 填写 00-项目定义/目标用户.md")
    print("  3. 填写 00-项目定义/栏目体系.md")
    print("  4. 使用 $book-architect 完善定位")
    print("  5. 有样文时使用 $book-reverse-style 做深反推")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
