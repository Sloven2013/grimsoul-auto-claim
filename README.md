**★1.2.0更新说明：官网更新，中文网址已失效，本次更新主要适配官网改版（包含英文界面）、优化领取逻辑，同时加固工作流。**
1. **网址更新**：旧的中文路径（`/zh/...`）全部 404，改为新的 `/rewards` 和 `/store`；并修复了 404 自动跳首页导致脚本 "假成功" 的问题。
2. **适配英文界面**：网站已无中文版，所有中文按钮文本改为英文文本和稳定的 `data-testid` 选择器；Cookie 弹窗改为关闭官网原生组件。
3. **登录流程适配新版**：支持两种登录入口 —— 主页内嵌的 User ID 表单和右上角 Log in 弹窗；增加登录结果校验和无效 ID 识别，不再固定等待。
4. **领取逻辑优化**：每日奖励通过 Claim 按钮领取、以倒计时判定已领取；免费塔勒通过 Get free 领取、以 Owned 状态判定成功，修复了原脚本全页匹配文本容易误判的问题。
5. **可靠性提升**：失败时返回非零退出码（Actions 会标红通知）、导航自动重试、任何异常路径都自动截图。
6. **工作流加固**：新增 `requirements.txt` 锁定 Playwright 版本，补充超时、权限和防重叠配置。

**✨ 功能特点**
全自动运行：每天定时启动，无需人工干预。

自动登录：只需填写游戏账号 ID（无需密码）。

智能 Cookie 处理：自动关闭 Cookie 弹窗。

精确领取：每日奖励检测倒计时，商店检测“免费”按钮。

自动截图：每次运行保存每日奖励和商店两张截图，方便核对。

运行日志：详细输出每一步操作，便于调试。


**🚀 快速开始**
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


**⏰ 定时运行说明**
默认设置为北京时间每天早上 08:06 运行（UTC 00:06）。

GitHub Actions 定时任务可能会有几分钟到几十分钟的延迟，这是正常现象。

如需修改时间，编辑 .github/workflows/claim.yml 中的 cron 表达式。常用换算：

北京时间 08:00 → UTC 00:00 → 0 0 * * *

北京时间 08:30 → UTC 00:30 → 30 0 * * *

北京时间 09:00 → UTC 01:00 → 0 1 * * *

**❓ 常见问题**
1. 运行日志显示“未找到可点击的按钮”
可能网站按钮文字发生了变化。请下载截图查看实际按钮文字，然后修改 claim.py 中对应的文本。

2. 如何手动运行？
在 Actions 页面点击 Run workflow 即可立即触发一次，不改变定时计划。

3. 会消耗 GitHub Actions 额度吗？
每次运行约 1 分钟，私有仓库每月有 2000 分钟免费额度，完全足够。

4. 账号 ID 安全吗？
账号 ID 保存在 GitHub Secrets 中，不会公开。但请确保仓库是 Private，避免他人访问你的 Actions 日志或截图。

5. 如果网站更新导致脚本失效怎么办？
可以提交 Issue 或自行修改 claim.py 中的选择器逻辑。

**注：目前已支持英文网站。**

📝 免责声明
本项目仅供学习交流使用，请遵守 Grim Soul 的服务条款。使用者需自行承担因使用本脚本可能带来的风险，包括但不限于账号被限制等。

---

# English Version

**★ v1.2.0 Update Notes: The official website has been rebuilt and the old Chinese URLs are no longer valid. This update adapts to the redesigned website (now in English), improves the claiming logic, and hardens the workflow.**
1. **Updated URLs**: The old Chinese paths (`/zh/...`) all return 404 and have been replaced by the new `/rewards` and `/store`. Also fixed the "false success" issue caused by the 404 page automatically redirecting to the homepage.
2. **English interface**: The site no longer has a Chinese version. All Chinese button text has been replaced with English text and stable `data-testid` selectors; cookie handling now closes the native cookie dialog.
3. **New login flow**: Supports two login methods — the inline User ID form on the homepage and the Log in modal in the top-right corner; adds login result verification and invalid-ID detection instead of fixed waiting.
4. **Improved claiming logic**: Daily rewards are claimed via the Claim button, with a countdown used to detect already-claimed status; free Thalers are claimed via Get free, with the Owned status used to confirm success. This fixes the issue where matching text across the whole page could cause false positives.
5. **Better reliability**: Returns a non-zero exit code on failure (Actions will be marked red and notify you), retries navigation automatically, and takes screenshots on any error path.
6. **Hardened workflow**: Added `requirements.txt` to pin the Playwright version, plus timeout, permission, and concurrency settings.

**✨ Features**
Fully automatic: runs on a schedule every day with no manual intervention.

Automatic login: only your game account ID is needed (no password).

Smart cookie handling: automatically closes the cookie dialog.

Precise claiming: checks the countdown for daily rewards and the "free" button in the store.

Automatic screenshots: saves two screenshots (daily rewards and store) each run for easy verification.

Logs: detailed output of every step for debugging.


**🚀 Quick Start**
Requirements
A [GitHub](https://github.com/) account

Your Grim Soul account ID (found in the game, e.g. XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX)

See the image below:
<img width="465" height="352" alt="image" src="https://github.com/user-attachments/assets/37b99bfb-fbed-47ae-b7c3-c4e3791aebd6" />

**Option 1: Fork this repository (easiest)**
Click the Fork button in the top-right corner to copy the repository to your GitHub account.

In your forked repository, go to Settings → Secrets and variables → Actions.

Click New repository secret and add:

Name: GRIMSOUL_ACCOUNT_ID

Value: your Grim Soul account ID

Click Add secret to save.

Go to the Actions tab. If prompted to enable workflows, click "I understand my workflows, go ahead and enable them."

Run a test manually: click Run workflow → Run workflow and check the logs for errors.

**Option 2: Create the files manually (if you don't want to fork)**
Create a new private repository on GitHub (e.g. grimsoul-auto-claim).

Add the GRIMSOUL_ACCOUNT_ID secret (same steps as above).

From this repository's code page, open claim.py and .github/workflows/claim.yml and copy their full contents.

In your new repository, create files with the same names and paste the contents:

claim.py goes in the repository root.

.github/workflows/claim.yml goes under the .github/workflows/ directory (note the directory structure).

After committing, go to the Actions page and run a test manually.

☆ Viewing screenshots
After a run, download the grimsoul-screenshots archive at the bottom of the Summary page. Extract it to get two screenshots, daily_rewards.png and store.png, to confirm the claiming status.

<img width="1280" height="720" alt="daily_rewards" src="https://github.com/user-attachments/assets/fb9fb64c-769a-40a9-8310-9e74fb14c53e" />

<img width="1280" height="720" alt="store" src="https://github.com/user-attachments/assets/867a75a3-6b0e-4271-a0ce-748feaeac499" />


**⏰ Scheduled Runs**
By default, runs at 08:06 Beijing time every day (00:06 UTC).

GitHub Actions scheduled runs may be delayed by several minutes or more; this is normal.

To change the time, edit the cron expression in .github/workflows/claim.yml. Common conversions:

08:00 Beijing → 00:00 UTC → 0 0 * * *

08:30 Beijing → 00:30 UTC → 30 0 * * *

09:00 Beijing → 01:00 UTC → 0 1 * * *

**❓ FAQ**
1. The logs say "no clickable button found"
The site's button text may have changed. Download the screenshots to check the actual text, then update the corresponding text in claim.py.

2. How do I run it manually?
On the Actions page, click Run workflow to trigger a run immediately without changing the schedule.

3. Does it consume GitHub Actions minutes?
Each run takes about 1 minute. Private repositories include 2,000 free minutes per month, which is more than enough.

4. Is my account ID safe?
The account ID is stored in GitHub Secrets and is not public. Make sure the repository is private to prevent others from accessing your Actions logs or screenshots.
5. What if the script stops working after a website update?
Open an issue or update the selectors in claim.py yourself.

**Note: The English website is currently supported.**

📝 Disclaimer
This project is for learning and communication purposes only. Please comply with Grim Soul's Terms of Service. Users bear all risks of using this script, including but not limited to account restrictions.
