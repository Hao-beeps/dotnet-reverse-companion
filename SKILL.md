---
name: dotnet-reverse-companion
description: 当用户需要分析一个 .NET / 桌面 GUI 程序（Windows 桌面工具、WPF/WinForms 应用、QQ 类客户端等）的内部实现、把 .exe/.dll 反编译为可读 C#、定位关键功能模块，或将竞品功能对齐复刻到自研项目时使用。覆盖反编译、关键模块定位、功能对齐检查表、代码注入复刻的完整方法论。关键词：.NET 反编译、IL、dnSpy、ILSpy、ilspycmd、逆向、竞品分析、功能对齐、行为复刻、桌面工具、QQ 接图。仅用于合法授权范围内的学习、互操作与安全研究。
---

# .NET 桌面应用逆向与功能对齐助手

帮助你把闭源 .NET 桌面程序的功能，以"行为层面高度一致"为目标，复刻 / 对齐到自研项目。本 skill 沉淀了一套六步闭环方法论，并附带两个辅助脚本。

## 何时使用

- 想把某个闭源 .NET 桌面工具的功能"复刻"到自研项目，且追求**行为对齐**而非浅层模仿
- 需要把一个 `.exe` / `.dll` 反编译成可读 C#，并定位关键功能模块
- 需要产出「竞品功能 → 自研实现」的**对齐检查表**
- 需要把提取的逻辑注入 / 移植到自研代码库，并验证兼容性
- 用户在讨论逆向、反编译、IL、dnSpy、ILSpy、竞品对标时

## 前置工具

- `ilspycmd`（推荐，命令行反编译）：`dotnet tool install --global ilspycmd`
- `dnSpy` / `dnSpyEx`（GUI，适合交互式浏览与导出）
- `dotnet`、`rg`（ripgrep，用于大规模代码检索）
- Python 3（运行本 skill 的辅助脚本）

## 六步闭环方法论

### Step 1 —— 目标定位与合规确认
先明确分析对象与授权边界：
- 只分析你**有权分析**的目标（自研竞品、已授权、或依法可逆向互操作的软件）
- 记录目标路径、版本号（如 `QQReceiveFile 20.0.5`），建一个工作目录存放扒取产物
- 产出：`目标清单.md`（路径、版本、用途、授权说明）

### Step 2 —— 反编译提取
优先用 `ilspycmd` 批量导出为 C#，便于后续检索：

```bash
# 导出单个程序集为 C#
ilspycmd -o ./decompiled/ TargetApp.exe

# 导出整个目录的所有 dll
mkdir -p ./decompiled && for f in TargetDir/*.dll; do
  ilspycmd -o "./decompiled/$(basename $f .dll)" "$f"
done
```

GUI 场景用 dnSpy 打开 → 右键程序集 → 导出到工程（保留原始命名空间与 IL 注释）。

### Step 3 —— 关键模块定位
在导出代码里用关键词收敛范围（不要通读全部）：

```bash
rg -n -i "receive|onmessage|hook|inject|clipboard|screenshot|config|timer" ./decompiled
```

按功能域归类（如"文件接收""消息监听""自动回复""注入点"），形成模块地图。

### Step 4 —— 功能对齐检查表
调用本 skill 的脚本，把上一步的功能点生成可追踪的对齐表：

```bash
python scripts/align_checklist.py --input features.txt --output 对齐检查表.md
```

`features.txt` 每行一个功能，可用 `!!高/中/低` 标注优先级。脚本输出 Markdown 表格：功能点 | 竞品行为 | 自研现状 | 优先级 | 状态。

### Step 5 —— 逻辑提取与移植
对每个对齐项：
1. 提取竞品对应 IL/C# 片段（保留签名与调用链）
2. 在自研项目写**等价实现**，目标是行为一致（用户偏好"全量、一模一样"）
3. 注意侵入性特性（如全局钩子、进程注入）需单独评估兼容与风险
4. 每完成一项，在检查表里把状态改为 ✅ 并附自研文件路径

### Step 6 —— 兼容性与功能验证
- 构建自研项目，确认无编译错误
- 运行并对比：逐项核对行为是否与竞品一致（尤其边界条件、错误路径）
- 记录未对齐项，回流到 Step 4 检查表

## 反编译命令速查

| 目的 | 命令 |
|------|------|
| 导出为 C# | `ilspycmd -o out/ app.exe` |
| 导出为 IL | `ilspycmd --il -o out/ app.exe` |
| 只看类型列表 | `ilspycmd --list-types app.exe` |
| 导出资源 | `ilspycmd --resource --no-dead-code -o out/ app.exe` |

## 合规边界（务必遵守）

- 本 skill 仅用于**合法授权范围内**的学习、互操作性研究、安全分析与自研启发
- 不得用于绕过授权、侵犯版权、破解付费限制或任何违法用途
- 复刻时优先自研等价实现，避免直接搬运受版权保护的专有代码
- 涉及进程注入 / 全局钩子等侵入性手段，需确认目标平台合规与用户知情同意

## 参考资源

- ILSpy 官方：`github.com/icsharpcode/ILSpy`
- dnSpyEx：`github.com/dnSpyEx/dnSpy`
- 本 skill 脚本：`scripts/align_checklist.py`、`scripts/decompile_helper.py`
