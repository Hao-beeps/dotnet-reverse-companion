# dotnet-reverse-companion

一个 **Claude Code / 类 agent 编程助手** 的 plugin：把闭源 .NET 桌面程序（WPF/WinForms、QQ 类客户端、Windows 工具）的功能，以"行为层面高度一致"为目标，复刻 / 对齐到自研项目。

沉淀自真实逆向工程实战（含 .NET IL 反编译、关键模块定位、全量功能对齐、代码注入复刻），把六步方法论 + **4 个辅助脚本**打包成一个开箱即用的 plugin。**进阶版定价 ¥59（微信，一次性，单档）。**

## 它解决什么痛点

- 拿到一个闭源 .NET 桌面工具，不知道从哪下手反编译
- 扒出一堆 C# 后，找不到关键功能在哪
- 复刻时没有一个可追踪的"竞品功能 ↔ 自研实现"对照表
- 移植完不知道哪些行为还没对齐、兼容性是否验证过

## 目录结构（Claude Code plugin 规范）

```
dotnet-reverse-companion/
├── .claude-plugin/
│   ├── plugin.json          # 插件清单（名称/版本/作者）
│   └── marketplace.json     # 原生 marketplace 声明（source: "./"）
├── skills/
│   └── dotnet-reverse-companion/
│       ├── SKILL.md         # skill 核心定义（模型读取）
│       └── scripts/
│           ├── align_checklist.py         # 生成功能对齐检查表
│           ├── decompile_helper.py        # 扫描程序集 + 生成反编译计划
│           ├── inject_template_generator.py  # [进阶] 从对齐表生成 C# 注入骨架
│           └── compat_report.py             # [进阶] 生成兼容性验证报告
├── LICENSE                  # MIT
├── README.md
└── STORE.md                 # 微信购买落地页 / 商品说明
```

## 安装到 Claude Code

本仓库本身就是一个 plugin，推荐走原生 marketplace 安装（一键安装 + 可更新）：

```bash
# 1. 把本仓库注册为 marketplace（owner/repo 换成你实际发布的地址）
claude plugin marketplace add 你的GitHub用户名/dotnet-reverse-companion

# 2. 从 marketplace 安装插件
claude plugin install dotnet-reverse-companion@asuc-plugins
```

> 若 Claude Code 提示，运行一次 `/reload-plugins` 即可激活。
> 要求 Claude Code v2.1.275+（安装） / v2.1.292+（单命令安装）。

**备用（手动）**：把 `skills/dotnet-reverse-companion/` 整个目录复制到 `~/.claude/skills/`（用户级）或 `.claude/skills/`（项目级），重启会话生效。

## 使用示例

```bash
# 进入 skill 目录
cd skills/dotnet-reverse-companion

# 1. 扫描目标，生成反编译计划
python scripts/decompile_helper.py --target ./QQReceiveFile_20.0.5/ --out plan.md

# 2. 按功能点生成对齐检查表（features.txt 每行一个功能，可加 高/中/低: 前缀）
python scripts/align_checklist.py --input features.txt --output 对齐检查表.md

# 3. [进阶] 把已 ✅ 的项生成注入骨架
python scripts/inject_template_generator.py --checklist 对齐检查表.md --out-dir injection_template

# 4. [进阶] 生成兼容性与功能验证报告
python scripts/compat_report.py --checklist 对齐检查表.md --output 兼容性报告.md
```

会话中直接说"帮我把这个 QQ 接图工具的功能复刻过来"，plugin 会自动触发本 skill。

## 合规边界（硬性红线）

- 仅用于**合法授权范围内**的学习、互操作性研究、安全分析与自研启发
- **红线一**：不规避 / 绕过任何软件的技术保护措施（加壳 / 加密 / 授权验证）
- **红线二**：不直接搬运专有代码；复刻须**自研等价实现**
- **红线三**：侵入性手段（注入 / 钩子）须确认合规与用户知情同意
- 使用者对自身合规负责，本插件不鼓励任何违法用途

---

## 上架指南（免费分发 · 当前状态：仓库已就绪，待推送 GitHub）

Claude Code 原生 marketplace 本质是**仓库根目录一个 `.claude-plugin/marketplace.json`**，push 到 GitHub 后即可被安装。本仓库文件已齐，但**尚未推送**——因为还未注册 GitHub 账号、本地也未安装 `gh`。注册完成后一键上架：

1. **注册 GitHub**（免费）：访问 github.com 注册账号，并记下用户名
2. **安装 gh**：https://cli.github.com/ 下载安装，或本机包管理器安装
3. **本地校验**（提交前必跑）：
   ```bash
   claude plugin validate .          # 常规校验
   claude plugin validate . --strict # 严格校验
   ```
4. **建仓库 + 推送**（把仓库级占位邮箱换成你自己的）：
   ```bash
   git config user.email "你@邮箱.com"
   gh repo create dotnet-reverse-companion --public --source=. --remote=origin --push
   ```
5. **用户自测闭环**：全新会话 `claude plugin marketplace add 你的用户名/dotnet-reverse-companion` → `claude plugin install dotnet-reverse-companion@asuc-plugins`，确认 skill 能触发、4 个脚本能跑
6. **可选投稿**：`anthropics/claude-plugins-community`（自动安全筛查）、HelloGitHub / 掘金、claudemarketplaces.com

> Anthropic 官方目录需**付费 claude.ai 计划**才能提交，且官方 curated 市场不接受第三方投稿。

---

## 售卖与收款（微信 · ¥59 进阶版 · 单档）

**关键事实**：Claude Code 原生 marketplace 的 spec **没有 price 字段——原生渠道只能免费分发，不能直接卖钱**（Anthropic 的设计决策）。所以售卖走**微信人民币收款 + 落地页引流**：

- **价格**：**¥59 进阶版（一次性，单档，永久使用）**，含全部 4 个脚本 + 方法论 + 安装说明 + 合规红线
- **收款**：微信转账 / 扫码（见 `STORE.md`，上线前把占位微信号换成你的真实收款方式）
- **交付**：付款后发插件压缩包 / 私有访问，附「5 分钟上手」图文 + 一次免费答疑
- **引流**：GitHub 免费展示 + 社区目录 + 中文渠道投稿，落地页指向微信购买

> 未来若想走加密支付，可把同一仓库提交到 **AgentStore**（`agentstore.dev`，USDC 一次性付费、80% 分润）或 **claudemarketplaces.com**（x402 付费 listing），但那需要钱包地址，当前阶段不强制。

---

## 下一步（落地清单）

- [x] 产品定位、plugin 结构、4 个脚本、合规红线、微信落地页 —— 已完成
- [ ] **注册 GitHub 账号 + 装 gh** —— 完成后我帮你建仓库 push（替换占位邮箱）
- [ ] **填微信收款方式** —— 把 `STORE.md` 里的占位微信号换成真实收款码
- [ ] **发布 / 引流** —— GitHub 公开 + 社区目录 + 中文渠道投稿，落地页挂微信购买

> 提示：定价与发布请以你自己的账号与合规判断为准。
