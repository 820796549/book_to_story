#!/usr/bin/env python3
"""Codex hooks for the book-to-article production system."""

from __future__ import annotations

import datetime as _dt
import json
import os
import sys
from pathlib import Path


def project_root() -> Path:
    env = os.environ.get("CODEX_PROJECT_DIR") or os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        return Path(env).resolve()

    cur = Path.cwd().resolve()
    for parent in [cur, *cur.parents]:
        if (parent / ".codex" / "hooks" / "book_codex_hook.py").exists():
            return parent
    return cur


def exists(root: Path, rel: str) -> bool:
    return (root / rel).exists()


def status(root: Path) -> list[str]:
    checks = [
        ("项目定位", "00-项目定义/书籍定位.md"),
        ("栏目体系", "00-项目定义/栏目体系.md"),
        ("栏目协议", "04-栏目协议"),
        ("样文反推", "01-样文反推"),
        ("原文拆解", "02-原文拆解"),
        ("模型提炼", "03-模型提炼"),
        ("文章成稿", "05-文章生产/成稿"),
        ("质量审查", "06-质量审查"),
    ]
    lines = ["[book] 拆有用书写文章生产系统"]
    for label, rel in checks:
        lines.append(f"- {label}: {'OK' if exists(root, rel) else '缺失'}")
    return lines


def session_start(root: Path) -> int:
    print("\n".join(status(root)))
    context = root / "追踪" / "上下文.md"
    if context.exists():
        print(f"[book] compact 后优先读取: {context}")
    return 0


def read_hook_payload() -> dict:
    try:
        raw = sys.stdin.read()
    except Exception:
        return {}
    if not raw.strip():
        return {}
    try:
        return json.loads(raw)
    except Exception:
        return {}


def payload_text(payload: dict) -> str:
    parts: list[str] = []
    for value in payload.values():
        if isinstance(value, str):
            parts.append(value)
        elif isinstance(value, dict):
            parts.append(payload_text(value))
        elif isinstance(value, list):
            parts.extend(str(item) for item in value)
    return "\n".join(parts)


def pre_tool_article_guard(root: Path) -> int:
    payload = read_hook_payload()
    text = payload_text(payload)
    normalized = text.replace("\\", "/")

    article_targets = [
        "05-文章生产/成稿",
        "05-文章生产/草稿",
    ]
    if not any(target in normalized for target in article_targets):
        return 0

    required = [
        "00-项目定义/书籍定位.md",
        "00-项目定义/栏目体系.md",
        "04-栏目协议",
        "01-样文反推",
        "02-原文拆解",
        "03-模型提炼",
    ]
    missing = [rel for rel in required if not exists(root, rel)]
    if not missing:
        return 0

    print("[book] 禁止直接写栏目文章：缺少前置材料。", file=sys.stderr)
    for rel in missing:
        print(f"- 缺失: {rel}", file=sys.stderr)
    print("[book] 请先完成书籍定位、栏目协议、样文反推、原文拆解和模型提炼。", file=sys.stderr)
    return 2


def pre_tool_commit_advisory(root: Path) -> int:
    """Check for common issues before commit. Warning only, not blocking."""
    warnings = []

    has_articles = exists(root, "05-文章生产/成稿")
    has_review = exists(root, "06-质量审查")
    has_positioning = exists(root, "00-项目定义/书籍定位.md")

    if has_articles and not has_review:
        warnings.append("有文章成稿但无质量审查目录")

    if has_articles and not has_positioning:
        warnings.append("有文章成稿但无书籍定位")

    if warnings:
        print("[book] commit 前检查发现以下问题（仅警告，不阻断）:")
        for w in warnings:
            print(f"  - {w}")

    return 0


def ensure_tracking(root: Path) -> Path:
    tracking = root / "追踪"
    tracking.mkdir(exist_ok=True)
    return tracking


def pre_compact(root: Path) -> int:
    tracking = ensure_tracking(root)
    context = tracking / "上下文.md"
    now = _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# 上下文快照",
        "",
        f"- 更新时间：{now}",
        "- 当前目标：拆有用书写文章，并让流程稳定复用。",
        "- 固定关系：竞品只学写法；oh-story 只做工程底座；毛选是第一套样板。",
        "",
        "## 项目状态",
        "",
        *status(root),
        "",
        "## 恢复顺序",
        "",
        "1. 读取 00-项目总纲/实施计划.md",
        "2. 读取 00-项目总纲/项目定位.md",
        "3. 读取 00-项目总纲/使用边界.md",
        "4. 再根据当前任务读取对应 skill 或项目文件",
    ]
    context.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[book] 已保存上下文快照: {context}")
    return 0


def post_compact(root: Path) -> int:
    context = root / "追踪" / "上下文.md"
    if context.exists():
        print(f"[book] 请优先读取上下文快照恢复状态: {context}")
    else:
        print("[book] 请优先读取 00-项目总纲/实施计划.md、项目定位.md、使用边界.md。")
    return 0


def stop(root: Path) -> int:
    """Log session end."""
    tracking = ensure_tracking(root)
    log = tracking / "session-log.md"
    now = _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"| {now} | 会话结束 | - | - |\n"
    if log.exists():
        with log.open("a", encoding="utf-8") as f:
            f.write(line)
    else:
        log.write_text("# 会话日志\n\n| 时间 | 完成内容 | 修改文件 | 当前阶段 |\n|---|---|---|---|\n" + line, encoding="utf-8")
    return 0


def main() -> int:
    root = project_root()
    action = sys.argv[1] if len(sys.argv) > 1 else "session-start"
    handlers = {
        "session-start": session_start,
        "pre-tool-article-guard": pre_tool_article_guard,
        "pre-tool-commit-advisory": pre_tool_commit_advisory,
        "pre-compact": pre_compact,
        "post-compact": post_compact,
        "stop": stop,
    }
    handler = handlers.get(action)
    if handler:
        return handler(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
