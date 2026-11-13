#!/usr/bin/env python3
"""兼容性 / 功能验证报告生成器（进阶版脚本之二）。

读取「功能对齐检查表.md」，统计对齐率、按优先级分布、
标记侵入性风险项，并产出一份可交付的验证报告 Markdown。

用法:
  python compat_report.py --checklist 对齐检查表.md --output 兼容性报告.md
  python compat_report.py --checklist 对齐检查表.md            # 输出到 stdout
  cat 对齐检查表.md | python compat_report.py -              # 从管道读取

合规: 本脚本仅汇总你填写的对齐状态，不读取或包含任何专有代码。
"""
import argparse
import sys
from datetime import date
from pathlib import Path

STATUS_DONE = "✅"
STATUS_WIP = "🚧"
STATUS_TODO = "⬜"
STATUS_REVIEW = "⚠️"
INTRUSIVE_HINTS = ("注入", "inject", "hook", "钩子", "进程", "全局", "劫持", "拦截")


def parse_checklist(text):
    rows = []
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6:
            continue
        if cells[0] in ("#",) or set(cells[0]) <= set("-: "):
            continue
        if not cells[0].isdigit():
            continue
        rows.append({
            "idx": cells[0], "priority": cells[1], "feature": cells[2],
            "rival": cells[3], "ours": cells[4], "status": cells[5],
        })
    return rows


def classify(row):
    s = row["status"]
    if STATUS_DONE in s:
        return "done"
    if STATUS_WIP in s:
        return "wip"
    if STATUS_REVIEW in s:
        return "review"
    return "todo"


def detect_intrusive(row):
    blob = (row["feature"] + row["rival"] + row["ours"]).lower()
    return [h for h in INTRUSIVE_HINTS if h.lower() in blob]


def render(rows):
    total = len(rows)
    counts = {"done": 0, "wip": 0, "review": 0, "todo": 0}
    prio = {"🔴 高": 0, "🟡 中": 0, "🟢 低": 0}
    intrusive = []
    for r in rows:
        counts[classify(r)] += 1
        if r["priority"] in prio:
            prio[r["priority"]] += 1
        hits = detect_intrusive(r)
        if hits:
            intrusive.append((r, hits))

    rate = (counts["done"] / total * 100) if total else 0
    today = date.today().isoformat()

    out = []
    out.append(f"# 兼容性与功能验证报告")
    out.append("")
    out.append(f"> 生成日期: {today}  |  功能总数: **{total}**  |  对齐率: **{rate:.0f}%**")
    out.append("")
    out.append("## 一、整体概览")
    out.append("")
    out.append("| 指标 | 数值 |")
    out.append("|------|------|")
    out.append(f"| 功能总数 | {total} |")
    out.append(f"| ✅ 已完成 | {counts['done']} |")
    out.append(f"| 🚧 进行中 | {counts['wip']} |")
    out.append(f"| ⚠️ 需评估 | {counts['review']} |")
    out.append(f"| ⬜ 待办 | {counts['todo']} |")
    out.append(f"| **对齐率** | **{rate:.0f}%** |")
    out.append("")
    out.append("## 二、按优先级分布")
    out.append("")
    out.append("| 优先级 | 数量 |")
    out.append("|--------|------|")
    for k, v in prio.items():
        out.append(f"| {k} | {v} |")
    out.append("")
    out.append("## 三、侵入性风险项")
    out.append("")
    if intrusive:
        out.append("| # | 功能点 | 命中关键词 | 建议 |")
        out.append("|---|--------|-----------|------|")
        for r, hits in intrusive:
            out.append(f"| {r['idx']} | {r['feature']} | {', '.join(hits)} | "
                       f"移植前单独评估兼容性与合规，确认授权与用户知情同意 |")
    else:
        out.append("未检测到注入 / 钩子 / 进程等侵入性关键词，风险较低。")
    out.append("")
    out.append("## 四、结论与建议")
    out.append("")
    if rate >= 90:
        out.append("- 对齐率 ≥ 90%，核心功能基本复刻完成，可进行发布前回归测试。")
    elif rate >= 50:
        out.append("- 对齐率 50%~90%，主干功能已完成，剩余项建议排期补齐后再发布。")
    else:
        out.append("- 对齐率 < 50%，仍处于早期移植阶段，不建议对外发布。")
    if intrusive:
        out.append("- 存在侵入性风险项，请在发布前逐一确认合规与兼容性，"
                   "优先采用非侵入的自研等价实现。")
    out.append("- 本报告仅汇总你填写的对齐状态，不包含任何专有代码；"
               "发布前请确保目标在合法授权范围内。")
    out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="生成兼容性与功能验证报告")
    ap.add_argument("--checklist", "-c", default="-", help="对齐检查表 md，或 '-' 从 stdin")
    ap.add_argument("--output", "-o", help="输出 md 路径（默认 stdout）")
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
    if not rows:
        print("[警告] 未解析到任何功能行。", file=sys.stderr)
    md = render(rows)

    if args.output:
        Path(args.output).write_text(md + "\n", encoding="utf-8")
        print(f"[完成] 已写入 {args.output}（{len(rows)} 个功能点）")
    else:
        print(md)


if __name__ == "__main__":
    main()
