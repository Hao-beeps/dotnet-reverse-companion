#!/usr/bin/env python3
"""自动注入模板生成器（进阶版脚本之一）。

读取「功能对齐检查表.md」，找出状态为 ✅ 已完成的项，
为每个对齐项生成一段 C# 注入点代码骨架（占位 + TODO），
并产出一份「注入清单.md」，帮助你把提取的逻辑有序地移植到自研项目。

用法:
  python inject_template_generator.py --checklist 对齐检查表.md --out-dir injection_template
  python inject_template_generator.py --checklist 对齐检查表.md          # 输出到 ./injection_template
  cat 对齐检查表.md | python inject_template_generator.py -             # 从管道读取

合规: 生成的仅为"等价实现"的代码骨架与占位，不搬运任何专有代码。
       实际实现请优先自研等价逻辑，并确认你有权分析与移植目标。
"""
import argparse
import re
import sys
from pathlib import Path

DONE_MARK = "✅"
INTRUSIVE_HINTS = ("注入", "inject", "hook", "钩子", "进程", "全局", "劫持", "拦截")


def parse_checklist(text):
    """解析对齐检查表 Markdown 表格，返回行字典列表。"""
    rows = []
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        # 列: # | 优先级 | 功能点 | 竞品行为 | 自研现状 | 状态
        if len(cells) < 6:
            continue
        if cells[0] in ("#",) or set(cells[0]) <= set("-: "):
            continue  # 表头或分隔行
        if not cells[0].isdigit():
            continue
        rows.append({
            "idx": cells[0],
            "priority": cells[1],
            "feature": cells[2],
            "rival": cells[3],
            "ours": cells[4],
            "status": cells[5],
        })
    return rows


def generate_cs(rows, out_dir: Path):
    parts = [
        "// =============================================================",
        "//  自动生成的注入点骨架（由 inject_template_generator.py 产出）",
        "//  说明: 以下仅为「等价实现」占位模板，不含任何专有代码。",
        "//  请优先自研等价逻辑；涉及注入/钩子等侵入性手段时，",
        "//  务必确认目标平台合规与用户知情同意。",
        "// =============================================================",
        "",
        "using System;",
        "using System.Collections.Generic;",
        "",
        "namespace ReverseCompanion.Injected",
        "{",
    ]
    for i, r in enumerate(rows, 1):
        feat = r["feature"]
        intrusive = any(h.lower() in (feat + r["rival"]).lower() for h in INTRUSIVE_HINTS)
        warn = "\n    // ⚠️ 侵入性特性: 移植前请单独评估兼容性与合规风险。" if intrusive else ""
        parts.append(f"    // ----- 注入项 {i}: {feat} -----")
        parts.append(f"    // 优先级: {r['priority']} | 状态: {r['status']}")
        if r["rival"] and r["rival"] not in ("❓",):
            parts.append(f"    // 竞品行为参考: {r['rival']}")
        parts.append(f"    public class InjectedFeature_{i}")
        parts.append("    {")
        parts.append(f"        // TODO: 实现「{feat}」的等价逻辑（自研，勿搬运专有代码）{warn}")
        parts.append("        public void Apply()")
        parts.append("        {")
        parts.append("            // 在此挂载到自研项目的对应生命周期/事件。")
        parts.append("        }")
        parts.append("    }")
        parts.append("")
    parts.append("}")
    parts.append("")
    (out_dir / "InjectedFeatures.cs").write_text("\n".join(parts), encoding="utf-8")


def generate_manifest(rows, out_dir: Path):
    lines = ["# 注入清单", "",
             f"> 共 {len(rows)} 个已完成对齐项待移植。", "",
             "| # | 优先级 | 功能点 | 注入类 | 侵入性 |",
             "|---|--------|--------|---------|--------|"]
    for i, r in enumerate(rows, 1):
        intrusive = any(h.lower() in (r["feature"] + r["rival"]).lower() for h in INTRUSIVE_HINTS)
        flag = "⚠️ 是" if intrusive else "—"
        lines.append(f"| {i} | {r['priority']} | {r['feature']} | `InjectedFeature_{i}` | {flag} |")
    lines.append("")
    lines.append("## 使用步骤")
    lines.append("1. 打开 `InjectedFeatures.cs`，逐项填充 `Apply()` 内的等价实现。")
    lines.append("2. 侵入性项（标记 ⚠️）先确认合规与兼容性，再决定是否挂载。")
    lines.append("3. 每完成一项，回写对齐检查表状态为 ✅ 并附自研文件路径。")
    lines.append("")
    (out_dir / "注入清单.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="从对齐检查表生成注入模板骨架")
    ap.add_argument("--checklist", "-c", default="-", help="对齐检查表 md，或 '-' 从 stdin")
    ap.add_argument("--out-dir", "-o", default="injection_template", help="输出目录")
    args = ap.parse_args()

    if args.checklist == "-":
        text = sys.stdin.read()
    else:
        p = Path(args.checklist)
        if not p.exists():
            print(f"[错误] 找不到检查表: {args.checklist}", file=sys.stderr)
            sys.exit(1)
        text = p.read_text(encoding="utf-8")

    rows = parse_checklist(text)
    done = [r for r in rows if DONE_MARK in r["status"]]
    if not rows:
        print("[警告] 未解析到任何功能行，请确认表格格式。", file=sys.stderr)
    if not done:
        print("[提示] 没有状态为 ✅ 的已完成项，未生成注入骨架。"
              "请先在对齐检查表里把要移植的项标记为 ✅。", file=sys.stderr)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    if done:
        generate_cs(done, out_dir)
        generate_manifest(done, out_dir)
        print(f"[完成] 已为 {len(done)} 个已完成项生成骨架 -> {out_dir}/")
    else:
        print("[完成] 未生成任何文件（无 ✅ 项）。", file=sys.stderr)


if __name__ == "__main__":
    main()
