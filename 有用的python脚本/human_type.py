import pyautogui
import time

def human_typing(text, delay=0.001):
    for char in text:
        pyautogui.typewrite(char)
        time.sleep(delay)

# 等待几秒钟以便你切换到目标应用程序
time.sleep(5)

# 像人类一样输入指定文字
human_typing('insect presence injury chest awareness extent strategy average society focus professor atmosphere penalty table datare commendation growth presentation reason cell breath cause department morning school risk ambition transportation wood president possibility head paper mode magazine director library wood school painting site poetry orange amount point historian television performance shirt effort photo coast possibility farmer mode internet location funeral salad guidance professor poem conversation solution management chocolate user independence university science explanation study health sistercousin ball concept homework instruction problem lady truthbook atmosphere language assistance moment difference recipe painting difficulty sign object machine passenger cousin resolution weakness rate morning class skill metal skill stock assumption significance version bird benefit power article radio game body priority fun conclusion guidance description charity risk candidate ratio drama')
