import uiautomation as auto
import pyautogui
import time

def wait_for_element(control, timeout=5):
    """等待元素出現"""
    start = time.time()
    while time.time() - start < timeout:
        if control.Exists(0.5):
            return True
    return False

def click_teams_icon():
    """透過 AutomationId 定位 Teams icon，點擊後往上 50、往右 30"""
    print("嘗試定位 Teams 圖示...")
    teams_icon = auto.ButtonControl(AutomationId="Appid: MSTeams_8wekyb3d8bbwe!MSTeams")
    time.sleep(2)

    if wait_for_element(teams_icon, 5):
        rect = teams_icon.BoundingRectangle
        center_x = (rect.left + rect.right) // 2
        center_y = (rect.top + rect.bottom) // 2

        # 移動到 Teams icon 並點擊
        pyautogui.moveTo(center_x, center_y, duration=0.2)
        print("🖱 滑鼠移到 Teams icon 並點擊")
        pyautogui.click(center_x, center_y)

        # 點擊後往上 50、往右 30
        offset_x = center_x + 30
        offset_y = center_y - 50
        time.sleep(0.5)
        pyautogui.click(offset_x, offset_y)
        print(f"✅ 已點擊偏移後座標: ({offset_x}, {offset_y})")
    else:
        print("⚠️ 找不到 Teams 圖示")
        exit()

def close_chat_popup():
    """檢查是否有『想要交談』的提示，若有則點擊叉叉"""
    print("🔍 檢查是否有交談提示框...")
    chat_popup = auto.TextControl(RegexName=".*想要交談.*")  # 偵測含有『想要交談』的文字
    
    if chat_popup.Exists(0.5):
        print("💬 偵測到交談提示")
        # 取得叉叉按鈕 (根據 AutomationId 或名稱)
        close_button = auto.ButtonControl(AutomationId="close_button")
        
        if close_button.Exists(0.5):
            close_button.Click()
            print("✅ 已點擊交談提示的叉叉")
        else:
            print("⚠️ 找不到交談提示的叉叉按鈕")
    else:
        print("ℹ️ 沒有交談提示")


def execute_flow():
    """執行主要流程"""
    # Step 1: 接受他人分享畫面
    print("嘗試接受他人分享畫面...")
    accept_share_button = auto.ButtonControl(Name="接受螢幕畫面分享")

    if wait_for_element(accept_share_button, 20):
        accept_share_button.Click()
        print("✅ 已接受分享畫面")
    else:
        print("⚠️ 找不到接受分享畫面的按鈕")
        return

    time.sleep(2)

    # Step 2: 點擊 share-button
    print("嘗試點擊 share-button...")
    share_button = auto.ButtonControl(AutomationId="share-button")

    if wait_for_element(share_button, 5):
        share_button.Click()
        print("✅ 已點擊 share-button")
    else:
        print("⚠️ 找不到 share-button")
        return

    time.sleep(2)

    # Step 3: 選擇「螢幕」
    print("嘗試定位 '螢幕' 文字...")
    screen_label = auto.TextControl(Name="螢幕")

    if wait_for_element(screen_label, 5):
        rect = screen_label.BoundingRectangle
        click_x = int((rect.left + rect.right) / 2)
        click_y = rect.bottom + 20
        pyautogui.click(click_x, click_y)
        print("✅ 已點擊螢幕縮圖")
    else:
        print("⚠️ 找不到 '螢幕' 標籤")
        return

    time.sleep(2)

    # Step 4: 透過 AutoId 喚醒 Teams
    click_teams_icon()

    time.sleep(15)
    # Step 4.5: 處理「想要交談」提示
    close_chat_popup()

    # Step 5: 點擊「授予控制權」（600 秒）
    print("嘗試點擊『授予控制權』（最多等 600 秒）...")
    grant_button = auto.ButtonControl(Name="授予控制權")

    if wait_for_element(grant_button, 600):
        grant_button.Click()
        print("✅ 已點擊『授予控制權』")
    else:
        print("⚠️ 600 秒內未找到『授予控制權』，需手動操作")


def main():
    print("📡 啟動自動監聽模式，等待 Teams 來電...")
    while True:
        accept_share_button = auto.ButtonControl(Name="接受螢幕畫面分享")
        if accept_share_button.Exists(0.5):
            print("🔔 偵測到有人分享螢幕，開始自動處理...")
            execute_flow()
            print("🏁 流程完成，回到監聽狀態")
        time.sleep(1)

if __name__ == "__main__":
    main()

