# 安装指引（买家版）

感谢购买「.NET 逆向复刻助手」Claude Code 插件。下面 3 步装好就能用。

## 前置条件
1. 已安装 **Claude Code**（或 Claude CLI）：https://claude.com/claude-code
2. 已安装 **.NET SDK**（反编译脚本需要）：
   - Windows：`winget install Microsoft.DotNet.SDK.8`
   - 或官网 https://dotnet.microsoft.com/download
3. 安装反编译器：`dotnet tool install --global ilspycmd`

## 安装方式（二选一）

### 方式 A：插件市场安装（推荐）
```bash
claude plugin marketplace add Hao-beeps/dotnet-reverse-companion
claude plugin install dotnet-reverse-companion@Hao-beeps
```

### 方式 B：手动复制到本地 skills 目录
把本压缩包里的 `skills/dotnet-reverse-companion/` 整个文件夹，
复制到以下任一位置：
- 项目级：`你的项目/.claude/skills/`
- 用户级：`~/.claude/skills/`

重启 Claude Code 会话即可生效。

## 怎么用（示例）
在 Claude Code 里直接说：
> 帮我把这个 QQ 接图工具的功能复刻到我自己的项目里

或让它生成对齐检查表：
> 用 dotnet-reverse-companion 给 xxx.dll 生成功能对齐检查表

它会自动调用本插件里的脚本和反编译流程。

## 遇到问题
- 脚本在 `skills/dotnet-reverse-companion/scripts/`，都是纯 Python，可单独运行。
- 详细文档见仓库 README.md。
- 售后：微信 `528127933`（购买凭证）。

## ⚠️ 合规红线（务必遵守）
本插件仅用于**合法授权范围内**的学习、互操作性研究、安全分析与自研启发。
- 不用于规避技术保护措施
- 不搬运受版权保护的专有代码（优先自研等价实现）
- 涉及进程注入/全局钩子等侵入性手段，须确认目标平台合规与用户知情同意
违规使用后果自负。
