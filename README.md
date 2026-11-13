# dotnet-reverse-companion

一个 **Claude Code / 类 agent 编程助手** 的 plugin：把闭源 .NET 桌面程序（WPF/WinForms、QQ 类客户端、Windows 工具）的功能，以"行为层面高度一致"为目标，复刻 / 对齐到自研项目。

沉淀自真实逆向工程实战（含 .NET IL 反编译、关键模块定位、全量功能对齐、代码注入复刻），把六步方法论 + 两个辅助脚本打包成一个开箱即用的 plugin。

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
│           ├── align_checklist.py     # 生成功能对齐检查表
│           └── decompile_helper.py    # 扫描程序集 + 生成反编译计划
├── LICENSE                  # MIT
└── README.md
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
```

会话中直接说"帮我把这个 QQ 接图工具的功能复刻过来"，plugin 会自动触发本 skill。

## 合规声明

本 skill 仅用于**合法授权范围内**的学习、互操作性研究、安全分析与自研启发。不得用于绕过授权、侵犯版权或任何违法用途。复刻时优先自研等价实现，避免直接搬运专有代码。

---

## 上架指南（免费分发）

Claude Code 的原生 marketplace 本质是**仓库根目录一个 `.claude-plugin/marketplace.json`**，push 到 GitHub 后即可被安装。本仓库已写好该文件，发布只需：

1. **本地校验**（强烈建议，避免提交后才发现 schema 错误）：
   ```bash
   claude plugin validate .          # 常规校验
   claude plugin validate . --strict # 严格校验（提交目录前用）
   ```
2. **推送 GitHub**：在仓库根 `git push` 到公开仓库（本仓库已是干净的 git 仓库，含 2 次提交 + `.gitignore`）。
3. **用户自测闭环**：在全新会话里 `claude plugin marketplace add 你的用户名/仓库` → `claude plugin install dotnet-reverse-companion@asuc-plugins`，确认 skill 能正常触发、两个脚本能跑——这是"真的能装"的唯一证据。
4. **可选投稿**：
   - 提交到 `anthropics/claude-plugins-community`（需通过自动安全筛查，不是官方 curated 市场但曝光高）
   - 投稿 HelloGitHub / 掘金 等中文渠道引 star
   - 在 claudemarketplaces.com 登记（社区目录，免费 listing）

> 注意：Anthropic 官方目录 `claude.ai/directory/manage` 需**付费 claude.ai 计划**才能提交，且官方 curated marketplace `claude-plugins-official` 不接受第三方提交。

---

## 卖钱指南（关键事实先说）

**Claude Code 原生 marketplace 的 spec 里没有 price 字段——原生渠道只能免费分发，不能直接卖钱。** 这是 Anthropic 的设计决策，不是漏了。所以"卖钱"要靠下面三条路：

### 路径 A：免费上架引流，靠后端变现（最稳）
- 原生 marketplace / 社区**免费**发布 plugin，作为获客与信任渠道
- 真正收费的是"增值服务"：
  - **定制逆向分析委托**（你已有实战经验，这是护城河；需确认合法授权）
  - **进阶付费版 skill**：加"自动注入模板生成""兼容性报告生成"等需要后端/算力的脚本
  - **配套视频 / 图文教程**（"我是如何把竞品功能 1:1 复刻到自研项目的"）

### 路径 B：第三方付费市场直接挂价
- **AgentStore**（`agentstore.dev`）：开源市场，支持 **USDC 一次性付费**，创作者拿 **80% 分润**，gasless 支付。免费 agent 免认证直接发，付费需 API key 或钱包签名。
- **claudemarketplaces.com**：社区市场，paid listing 走 **x402 加密支付**（USDC/USDG），需 6 项审查通过后发布。

### 路径 C：免费插件 + 收费 SaaS（长期复利）
经典模式（Readwise、Copilot Plus 都这么干）：plugin 是**免费客户端**，背后接一个**按订阅/用量收费的服务**（插件用 API key 鉴权，收费在服务器侧）。需要你自建后端，门槛高但最可持续。

> 本 skill 是纯本地脚本、无后端，路径 A / B 最现实。建议先走 A 免费引流 + 定制委托，跑通后再考虑 B 挂价。

---

## 下一步（需你拍板 / 授权）

- [ ] **GitHub 账号**：给我用户名或让我走 `gh login`，我帮你建仓库 + push（改掉仓库级占位邮箱 `asuc@workbuddy.local`）
- [ ] **是否挂付费**：决定走路径 A（免费引流）还是 B（AgentStore 挂价 $5–19）
- [ ] **钱包地址**（若走 B 的 USDC 分润）：提供一个以太坊地址收 USDC
- [ ] **定价**：一次性 $5 / $9 / $19，或按委托工时收费

> 提示：定价与发布请以你自己的账号与合规判断为准。
