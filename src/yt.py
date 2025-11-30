import pyautogui


def youtube_search(
    query: str,
):
    pyautogui.sleep(0.5)
    pyautogui.hotkey('win', 'b')
    pyautogui.sleep(0.1)
    pyautogui.hotkey('alt', 'd')
    pyautogui.sleep(0.1)
    pyautogui.typewrite("youtube.com" + " ", interval=0.01)
    pyautogui.sleep(0.1)
    pyautogui.press("enter")
    pyautogui.sleep(5)
    pyautogui.press("/")
    pyautogui.sleep(0.1)
    pyautogui.typewrite(query + " ", interval=0.01)
    pyautogui.sleep(0.1)
    pyautogui.press("enter")
    pyautogui.sleep(5)
    pyautogui.click(x=2531, y=340)

    return
