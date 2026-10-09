**★1.1.0更新说明：增加一个处理促销弹窗的步骤。加入了一个新函数 handle_promo_popup，并在 login 函数中调用**



✨ 功能特点
全自动运行：每天定时启动，无需人工干预。

自动登录：只需填写游戏账号 ID（无需密码）。

智能 Cookie 处理：自动关闭 Termly Cookie 弹窗。

精确领取：每日奖励检测倒计时，商店检测“免费”按钮。

自动截图：每次运行保存每日奖励和商店两张截图，方便核对。

运行日志：详细输出每一步操作，便于调试。


🚀 快速开始
前置要求
一个 [GitHub](https://github.com/) 账号

你的 Grim Soul 账号 ID（可以在游戏内找到，例如: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX）

可参考下图：
<img width="465" height="352" alt="image" src="https://github.com/user-attachments/assets/37b99bfb-fbed-47ae-b7c3-c4e3791aebd6" />

**方式一：Fork 本仓库（最简单）**
点击本仓库右上角的 Fork 按钮，将仓库复制到你的 GitHub 账号下。

进入你 Fork 后的仓库，点击 Settings → Secrets and variables → Actions。

点击 New repository secret，添加：

Name: GRIMSOUL_ACCOUNT_ID

Value: 你的 Grim Soul 账号 ID

点击 Add secret 保存。

进入 Actions 标签页，如果提示启用工作流，点击 I understand my workflows, go ahead and enable them。

手动运行一次测试：点击 Run workflow → Run workflow，确认日志无报错。

**方式二：手动创建文件（适合不想 Fork 的情况）**
在 GitHub 上新建一个 Private 仓库（例如 grimsoul-auto-claim）。

添加 Secret GRIMSOUL_ACCOUNT_ID（步骤同上）。

从本仓库的代码页面，分别打开 claim.py 和 .github/workflows/claim.yml，复制其完整内容。

在你的新仓库中，创建同名文件并粘贴内容：

claim.py 放在仓库根目录。

.github/workflows/claim.yml 放在 .github/workflows/ 目录下（注意目录结构）。

提交后，进入 Actions 页面手动运行一次测试。

☆查看截图
运行结束后，在 Summary 页面底部可以下载 grimsoul-screenshots 压缩包，解压后得到两张截图：daily_rewards.png 和 store.png，用于确认领取状态。

<img width="1280" height="720" alt="daily_rewards" src="https://github.com/user-attachments/assets/fb9fb64c-769a-40a9-8310-9e74fb14c53e" />

<img width="1280" height="720" alt="store" src="https://github.com/user-attachments/assets/867a75a3-6b0e-4271-a0ce-748feaeac499" />


⏰ 定时运行说明
默认设置为北京时间每天早上 08:00 运行（UTC 00:00）。

GitHub Actions 定时任务可能会有几分钟到几十分钟的延迟，这是正常现象。

如需修改时间，编辑 .github/workflows/claim.yml 中的 cron 表达式。常用换算：

北京时间 08:00 → UTC 00:00 → 0 0 * * *

北京时间 08:30 → UTC 00:30 → 30 0 * * *

北京时间 09:00 → UTC 01:00 → 0 1 * * *

❓ 常见问题
1. 运行日志显示“未找到可点击的按钮”
可能网站按钮文字发生了变化。请下载截图查看实际按钮文字，然后修改 claim.py 中对应的文本列表（例如 DAILY_CLAIM_TEXT 或 STORE_FREE_TEXT）。

2. 如何手动运行？
在 Actions 页面点击 Run workflow 即可立即触发一次，不改变定时计划。

3. 会消耗 GitHub Actions 额度吗？
每次运行约 1 分钟，私有仓库每月有 2000 分钟免费额度，完全足够。

4. 账号 ID 安全吗？
账号 ID 保存在 GitHub Secrets 中，不会公开。但请确保仓库是 Private，避免他人访问你的 Actions 日志或截图。

5. 如果网站更新导致脚本失效怎么办？
可以提交 Issue 或自行修改 claim.py 中的选择器逻辑。

**注：本脚本仅支持在中文网站领取，英文网站暂不支持。**

📝 免责声明
本项目仅供学习交流使用，请遵守 Grim Soul 的服务条款。使用者需自行承担因使用本脚本可能带来的风险，包括但不限于账号被限制等。
