# dotnet-reverse-companion

一个 **Claude Code / 类 agent 编程助手** 的 skill：把闭源 .NET 桌面程序（WPF/WinForms、QQ 类客户端、Windows 工具）的功能，以"行为层面高度一致"为目标，复刻 / 对齐到自研项目。

沉淀自真实逆向工程实战（含 .NET IL 反编译、关键模块定位、全量功能对齐、代码注入复刻），把六步方法论 + 两个辅助脚本打包成一个开箱即用的 skill。

## 它解决什么痛点

- 拿到一个闭源 .NET 桌面工具，不知道从哪下手反编译
- 扒出一堆 C# 后，找不到关键功能在哪
- 复刻时没有一个可追踪的"竞品功能 ↔ 自研实现"对照表
- 移植完不知道哪些行为还没对齐、兼容性是否验证过

## 目录结构

```
dotnet-reverse-companion/
├── SKILL.md                       # skill 核心定义（模型读取）
├── scripts/
│   ├── align_checklist.py         # 生成功能对齐检查表
│   └── decompile_helper.py        # 扫描程序集 + 生成反编译计划
└── README.md
```

## 安装到 Claude Code

把整个目录放到 Claude Code 的 skills 路径之一：

```bash
# 用户级（所有项目可用）
cp -r dotnet-reverse-companion ~/.claude/skills/

# 或项目级（仅当前仓库）
cp -r dotnet-reverse-companion ./.claude/skills/
```

重启 / 新建 Claude Code 会话后，当你说"帮我把这个 QQ 接图工具的功能复刻过来"，它就会自动调用本 skill。

## 使用示例

```bash
# 1. 扫描目标，生成反编译计划
python scripts/decompile_helper.py --target ./QQReceiveFile_20.0.5/ --out plan.md

# 2. 按功能点生成对齐检查表（features.txt 每行一个功能，可加 高/中/低: 前缀）
python scripts/align_checklist.py --input features.txt --output 对齐检查表.md
```

## 合规声明

本 skill 仅用于**合法授权范围内**的学习、互操作性研究、安全分析与自研启发。不得用于绕过授权、侵犯版权或任何违法用途。复刻时优先自研等价实现，避免直接搬运专有代码。

## 上架 / 变现建议

1. **GitHub 开源 + 星标引流**：发布到 GitHub，写清楚"逆向方法论 + 实战案例"，吸引开发者 star（参考 HelloGitHub 等渠道投稿）
2. **社区上架**：提交到 Claude Code skills 社区 / awesome-claude-skills 列表
3. **进阶变现**：
   - 付费版增加"自动化注入模板生成""兼容性报告生成"等高级脚本
   - 配套视频/图文教程（如"我是如何把竞品功能 1:1 复刻到自研项目的"）
   - 接受定制逆向分析委托（需确认合法授权）

> 提示：定价与发布请以你自己的账号与合规判断为准。
