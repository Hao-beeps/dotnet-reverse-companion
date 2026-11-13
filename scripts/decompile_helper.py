#!/usr/bin/env python3
"""扫描目标程序集并生成反编译分析计划（Markdown）。

用法:
  python decompile_helper.py --target ./TargetApp/
  python decompile_helper.py --target TargetApp.exe --out plan.md

会:
  1. 列出目录下所有 .exe / .dll（可识别版本信息文件名）
  2. 检测本机是否已安装 ilspycmd / dnSpy
  3. 输出一份可直接执行的「反编译计划」Markdown
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

EXTS = (".exe", ".dll")


def find_assemblies(target):
    t = Path(target)
    if t.is_file():
        return [t]
    return sorted([p for p in t.rglob("*") if p.suffix.lower() in EXTS],
                  key=lambda p: p.name.lower())


def detect_tools():
    tools = {}
    for name in ("ilspycmd", "dnSpy", "dnSpy.exe", "dotnet"):
        path = shutil.which(name)
        tools[name] = path or "(未安装)"
    return tools


def build_plan(target, assemblies, tools):
    lines = ["# 反编译分析计划", "", f"- 目标: `{target}`",
             f"- 程序集数量: {len(assemblies)}", "",
             "## 环境检测", ""]
    for k, v in tools.items():
        lines.append(f"- `{k}`: {v}")
    lines += ["", "## 待分析程序集", "",
              "| # | 文件 | 建议命令 |", "|---|------|----------|"]
    for i, a in enumerate(assemblies, 1):
        lines.append(f"| {i} | `{a.name}` | `ilspycmd -o ./decompiled/{a.stem} \"{a}\"` |")
    ilspy = tools.get("ilspycmd", "")
    lines += ["", "## 一键批处理", "", "```bash"]
    if ilspy and ilspy != "(未安装)":
        for a in assemblies:
            lines.append(f'ilspycmd -o "./decompiled/{a.stem}" "{a}"')
    else:
        lines.append("# 未检测到 ilspycmd，请先安装: dotnet tool install --global ilspycmd")
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="生成反编译分析计划")
    ap.add_argument("--target", "-t", required=True, help="目标 exe 文件或目录")
    ap.add_argument("--out", "-o", help="输出 Markdown 路径（默认 stdout）")
    args = ap.parse_args()

    if not Path(args.target).exists():
        print(f"[错误] 目标不存在: {args.target}", file=sys.stderr)
        sys.exit(1)

    assemblies = find_assemblies(args.target)
    if not assemblies:
        print(f"[警告] 在 {args.target} 下未发现 .exe/.dll", file=sys.stderr)
    tools = detect_tools()
    md = build_plan(args.target, assemblies, tools)

    if args.out:
        Path(args.out).write_text(md + "\n", encoding="utf-8")
        print(f"[完成] 已写入 {args.out}（{len(assemblies)} 个程序集）")
    else:
        print(md)


if __name__ == "__main__":
    main()
