#!/usr/bin/env python3
"""生成「竞品功能 -> 自研实现」对齐检查表（Markdown）。

用法:
  python align_checklist.py --input features.txt --output 对齐检查表.md
  python align_checklist.py --input features.txt            # 输出到 stdout
  cat features.txt | python align_checklist.py -           # 从管道读取

features.txt 每行一个功能，可用前缀标注优先级:
  高:接收QQ图片
  中:自动重命名
  !!低:托盘图标

优先级前缀支持: 高 / 中 / 低 / !!高 / !!中 / !!低
"""
import argparse
import sys
from pathlib import Path

PRIORITY_MAP = {
    "高": "🔴 高",
    "中": "🟡 中",
    "低": "🟢 低",
}


def parse_features(lines):
    rows = []
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        priority = "🟡 中"
        text = line
        # 支持 "高:xxx" 或 "!!高:xxx"
        if ":" in line:
            head, rest = line.split(":", 1)
            head = head.replace("!", "").strip()
            if head in PRIORITY_MAP:
                priority = PRIORITY_MAP[head]
                text = rest.strip()
        rows.append((priority, text))
    return rows


def render_md(rows):
    out = ["# 功能对齐检查表", "",
           "| # | 优先级 | 功能点 | 竞品行为（待填） | 自研现状 | 状态 |",
           "|---|--------|--------|----------------|----------|------|"]
    for i, (prio, text) in enumerate(rows, 1):
        out.append(f"| {i} | {prio} | {text} | ❓ | — | ⬜ 待办 |")
    out.append("")
    out.append("> 状态图例: ⬜ 待办 · 🚧 进行中 · ✅ 已完成 · ⚠️ 需评估")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="生成功能对齐检查表")
    ap.add_argument("--input", "-i", default="-",
                    help="功能列表文件，或 '-' 从 stdin 读取")
    ap.add_argument("--output", "-o", help="输出 Markdown 路径（默认 stdout）")
    args = ap.parse_args()

    if args.input == "-":
        lines = sys.stdin.readlines()
    else:
        p = Path(args.input)
        if not p.exists():
            print(f"[错误] 找不到输入文件: {args.input}", file=sys.stderr)
            sys.exit(1)
        lines = p.read_text(encoding="utf-8").splitlines()

    rows = parse_features(lines)
    if not rows:
        print("[警告] 没有解析到任何功能点。", file=sys.stderr)
    md = render_md(rows)

    if args.output:
        Path(args.output).write_text(md + "\n", encoding="utf-8")
        print(f"[完成] 已写入 {args.output}（{len(rows)} 个功能点）")
    else:
        print(md)


if __name__ == "__main__":
    main()
