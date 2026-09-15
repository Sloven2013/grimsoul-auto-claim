import os
import re
import json
import datetime
from playwright.sync_api import sync_playwright

ACCOUNT_ID = os.environ.get("GRIMSOUL_ACCOUNT_ID")
DAILY_URL = "https://grimsoul.com/zh/daily-rewards"
STORE_URL = "https://grimsoul.com/zh/store"

# 每日奖励按钮文字
DAILY_CLAIM_TEXT = "领取"

# 商店免费按钮文字
STORE_FREE_TEXT = "免费"

# 弹窗成功文本
SUCCESS_TEXTS = ["恭喜", "获得", "成功", "领取成功", "奖励", "You got", "Received", "Success", "Congratulations"]
# 弹窗已领取文本
ALREADY_TEXTS = ["已领取", "已经领取", "已签到", "Already claimed", "Claimed", "Come back tomorrow"]

def log(msg):
    print(f"[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] {msg}")

def handle_promo_popup(page):
    """处理促销活动弹窗（Activate/关闭）"""
    log("检测是否有促销活动弹窗...")
    
    # 1. 尝试点击 'Activate' 按钮（如果点击它会直接关闭弹窗并激活折扣）
    activate_texts = ["Activate", "激活", "Activate Now"]
    for text in activate_texts:
        try:
            loc = page.locator(f'button:has-text("{text}"), a:has-text("{text}")').first
            if loc.is_visible() and loc.is_enabled():
                loc.click(timeout=3000)
                log(f"已点击促销弹窗按钮：{text}")
                page.wait_for_timeout(2000) # 等待弹窗消失
                return True
        except:
            continue

    # 2. 如果找不到 Activate，尝试点击右上角的关闭按钮（×）
    close_selectors = [
        'button[aria-label="Close"]',
        'button[aria-label="关闭"]',
        'button:has-text("×")',
        'div[role="button"]:has-text("×")',
        'span:has-text("×")',
        '[class*="close"]',
        '[class*="Close"]',
        '.close-icon'
    ]
    for sel in close_selectors:
        try:
            loc = page.locator(sel).first
            if loc.is_visible() and loc.is_enabled():
                loc.click(timeout=3000)
                log(f"已点击促销弹窗关闭按钮：{sel}")
                page.wait_for_timeout(2000)
                return True
        except:
            continue

    # 3. 兜底：尝试直接点击页面上的 "×" 文本
    try:
        loc = page.get_by_text("×", exact=True).first
        if loc.is_visible():
            loc.click(timeout=3000)
            log("已通过文本点击关闭按钮：×")
            page.wait_for_timeout(2000)
            return True
    except:
        pass

    log("未找到促销活动弹窗，或已自动消失")
    return False

def handle_cookie_banner(page):
    """精准处理 Termly Cookie 弹窗"""
    dialog_selectors = [
        'div[class*="termly"]', 'div[class*="cookie"]', 'div[class*="consent"]',
        'div[id*="termly"]', 'div[id*="cookie"]', 'div[id*="consent"]',
        '[role="dialog"]', '.modal', '.popup', '.dialog'
    ]
    primary_buttons = ["Allow All", "允许所有", "全部允许", "Decline All", "拒绝所有", "全部拒绝"]
    secondary_buttons = ["Accept All", "Accept", "同意", "接受", "允许"]

    container = None
    for sel in dialog_selectors:
        try:
            loc = page.locator(sel).first
            if loc.is_visible():
                container = loc
                log(f"找到 Cookie 弹窗容器：{sel}")
                break
        except:
            continue

    if container:
        for text in primary_buttons:
            try:
                btn = container.locator(f'button:has-text("{text}")').first
                if btn.is_visible() and btn.is_enabled():
                    btn.click(timeout=2000)
                    log(f"在弹窗内点击按钮：{text}")
                    page.wait_for_timeout(1000)
                    if not container.is_visible():
                        log("Cookie 弹窗已关闭")
                        return True
            except:
                continue
        for text in secondary_buttons:
            try:
                btn = container.locator(f'button:has-text("{text}")').first
                if btn.is_visible() and btn.is_enabled():
                    btn.click(timeout=2000)
                    log(f"在弹窗内点击按钮：{text}")
                    page.wait_for_timeout(1000)
                    if not container.is_visible():
                        log("Cookie 弹窗已关闭")
                        return True
            except:
                continue

    for text in primary_buttons + secondary_buttons:
        try:
            btn = page.locator(f'button:has-text("{text}")').first
            if btn.is_visible() and btn.is_enabled():
                btn.click(timeout=2000)
                log(f"全局点击按钮：{text}")
                page.wait_for_timeout(1000)
                return True
        except:
            continue

    return False

def has_countdown(page):
    """检测页面是否存在倒计时格式（如 12:34:56）"""
    try:
        result = page.evaluate("""
            () => {
                const regex = /^\\d{1,2}:\\d{2}:\\d{2}$/;
                const all = document.querySelectorAll('body *');
                for (const el of all) {
                    if (el instanceof HTMLElement) {
                        const style = window.getComputedStyle(el);
                        if (style.display !== 'none' && style.visibility !== 'hidden' && el.offsetWidth > 0) {
                            const text = el.innerText.trim();
                            if (text && regex.test(text)) return text;
                        }
                    }
                }
                return null;
            }
        """)
        if result:
            log(f"检测到倒计时文本：'{result}'")
            return True
        return False
    except Exception as e:
        log(f"倒计时检测出错：{e}")
        return False

def get_visible_text(page, selector='body'):
    try:
        return page.inner_text(selector)
    except:
        return ""

def click_button_with_text(page, text):
    """查找包含指定文本的可点击按钮并点击"""
    for selector in ["button", "a", "[role=button]"]:
        try:
            locs = page.locator(f'{selector}:has-text("{text}")')
            count = locs.count()
            for i in range(count):
                loc = locs.nth(i)
                if loc.is_visible() and loc.is_enabled():
                    loc.click(timeout=3000)
                    log(f"点击了包含“{text}”的按钮（选择器 {selector}）")
                    return True
        except:
            continue
    # 兜底：通过文本直接点击
    try:
        loc = page.get_by_text(text, exact=False).first
        if loc.is_visible() and loc.is_enabled():
            loc.click(timeout=3000)
            log(f"通过文本点击了“{text}”")
            return True
    except:
        pass
    log(f"未找到包含“{text}”的可点击按钮")
    return False

def wait_and_check_popup(page, timeout=8000):
    popup_selectors = ['.modal', '.popup', '.dialog', '[role="dialog"]', '.toast', '.notification',
                       'div[class*="modal"]', 'div[class*="popup"]', 'div[class*="dialog"]']
    try:
        page.wait_for_selector(popup_selectors[0], timeout=timeout)
    except:
        page.wait_for_timeout(timeout)
    visible_text = get_visible_text(page).lower()
    if any(t.lower() in visible_text for t in ALREADY_TEXTS):
        log("弹窗提示：已领取")
        return 'already'
    if any(t.lower() in visible_text for t in SUCCESS_TEXTS):
        log("弹窗提示：领取成功")
        return 'success'
    log("弹窗内容未知，可能已领取或领取成功")
    return 'unknown'

def login(page):
    page.goto("https://grimsoul.com/zh", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(2000)
    
    # 处理 Cookie 弹窗
    handle_cookie_banner(page)
    
    # 处理促销弹窗
    handle_promo_popup(page)

    login_clicked = False
    for text in ["登录", "登入", "Login", "Sign in"]:
        try:
            loc = page.get_by_text(text, exact=False).first
            if loc.is_visible():
                loc.click(timeout=3000)
                log(f"点击登录按钮：{text}")
                login_clicked = True
                break
        except:
            continue
    if not login_clicked:
        for sel in ['button:has-text("登录")', 'a:has-text("登录")', '[data-testid="login"]', '.login-btn', '#loginBtn']:
            try:
                loc = page.locator(sel).first
                if loc.is_visible():
                    loc.click(timeout=3000)
                    log(f"点击登录按钮（选择器：{sel}）")
                    login_clicked = True
                    break
            except:
                continue
    if not login_clicked:
        log("警告：未找到登录按钮，请检查页面结构")
        return False

    page.wait_for_timeout(2000)

    input_found = False
    input_selectors = ['input[type="text"]', 'input[type="email"]', 'input:not([type="hidden"])',
                       'input[placeholder*="账号"]', 'input[placeholder*="ID"]',
                       'input[placeholder*="Account"]', 'input[placeholder*="id"]', 'input[placeholder*="账户"]']
    for sel in input_selectors:
        try:
            loc = page.locator(sel).first
            if loc.is_visible() and loc.is_enabled():
                loc.fill(ACCOUNT_ID)
                log(f"已填写账号 ID 到输入框（选择器：{sel}）")
                input_found = True
                break
        except:
            continue
    if not input_found:
        log("错误：未找到账号输入框")
        return False

    submit_clicked = False
    for text in ["确认", "提交", "进入", "登录", "OK", "Submit", "Confirm", "Enter"]:
        try:
            loc = page.get_by_text(text, exact=False).first
            if loc.is_visible() and loc.is_enabled():
                loc.click(timeout=3000)
                log(f"点击确认按钮：{text}")
                submit_clicked = True
                break
        except:
            continue
    if not submit_clicked:
        try:
            page.keyboard.press("Enter")
            log("已按回车键提交登录")
            submit_clicked = True
        except:
            pass
    if not submit_clicked:
        log("错误：未找到确认按钮")
        return False

    page.wait_for_timeout(3000)
    log("登录完成")
    return True

def main():
    if not ACCOUNT_ID:
        log("错误：未找到 GRIMSOUL_ACCOUNT_ID 环境变量")
        return

    log("===== 开始执行自动领取 =====")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(locale="zh-CN")
        page = context.new_page()

        if not login(page):
            log("登录失败，脚本终止")
            browser.close()
            return

        # ========== 每日奖励页面 ==========
        log("访问每日奖励页面")
        page.goto(DAILY_URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(3000)
        handle_cookie_banner(page)
        # ★ 关键修改：进入每日奖励页面后，也要检测并关闭促销弹窗
        handle_promo_popup(page)

        if has_countdown(page):
            log("每日奖励：检测到倒计时，跳过")
        else:
            log("每日奖励：无倒计时，尝试点击“领取”按钮")
            if click_button_with_text(page, DAILY_CLAIM_TEXT):
                log("每日奖励：已点击“领取”按钮，等待弹窗...")
                result = wait_and_check_popup(page)
                if result == 'success':
                    log("每日奖励：领取成功！")
                elif result == 'already':
                    log("每日奖励：今天已领取过，无需重复操作")
                else:
                    log("每日奖励：弹窗内容未知，请手动检查")
            else:
                log("每日奖励：未找到“领取”按钮")

        # 每日奖励截图
        try:
            page.screenshot(path="/tmp/daily_rewards.png")
            log("已保存每日奖励截图：/tmp/daily_rewards.png")
        except:
            log("每日奖励截图失败")

        # ========== 商店免费硬币页面 ==========
        log("访问商店页面")
        page.goto(STORE_URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(3000)
        handle_cookie_banner(page)
        # ★ 关键修改：进入商店页面后，也要检测并关闭促销弹窗
        handle_promo_popup(page)

        # 商店逻辑：检查是否有“已领取”文本，没有则点击“免费”按钮
        body_text = get_visible_text(page).lower()
        store_has_claimed = any(t.lower() in body_text for t in ALREADY_TEXTS)
        if store_has_claimed:
            log("商店：检测到已领取文本，跳过")
        else:
            log("商店：未检测到已领取文本，尝试点击“免费”按钮")
            if click_button_with_text(page, STORE_FREE_TEXT):
                log("商店：已点击“免费”按钮，等待弹窗...")
                result = wait_and_check_popup(page)
                if result == 'success':
                    log("商店：免费硬币领取成功！")
                elif result == 'already':
                    log("商店：今天已领取过，无需重复操作")
                else:
                    log("商店：弹窗内容未知，请手动检查")
            else:
                log("商店：未找到可点击的“免费”按钮")

        # 商店截图
        try:
            page.screenshot(path="/tmp/store.png")
            log("已保存商店截图：/tmp/store.png")
        except:
            log("商店截图失败")

        browser.close()

    log("===== 任务结束 =====")

if __name__ == "__main__":
    main()
