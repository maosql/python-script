import os
import sys
import pyautogui
import pyperclip
import time
import datetime

d1 = datetime.datetime(2021, 8, 2)

d2 = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)

dayCount = (d2 - d1).days

# localtime = time.localtime(time.time())



# def get_msg():
#     """想发的消息，每条消息空格分开"""
#     contents = "狗 狗 狗 狗"
#     return contents.split(" ")

dayCount = str(dayCount)
msg = "Early, love time:" + dayCount

# send_card_link(self,
#                 self_wx = "maosql1",
#                 to_wx = "L-lik-only",
#                 title = "hhh",
#                 desc = "xxx",
#                 target_url = "http://baidu.com",
#                 img_url = "http://img.czdsh.com/Fsc_C6Rz5Sk7sblr_Q4YI0Y9v0zb"
# )

def send(msg):
    # 复制需要发送的内容到粘贴板
    pyperclip.copy(msg)
    # 模拟键盘 ctrl + v 粘贴内容
    pyautogui.hotkey('ctrl', 'v')
    # 发送消息
    pyautogui.press('enter')


def send_msg(friend):
    # Ctrl + alt + w 打开微信
    pyautogui.hotkey('ctrl', 'shift', 'w')
    # 搜索好友
    pyautogui.hotkey('ctrl', 'f')
    # 复制好友昵称到粘贴板
    pyperclip.copy(friend)
    # 模拟键盘 ctrl + v 粘贴
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    # 回车进入好友消息界面
    pyautogui.press('enter')

    #发送一条消息
    send(msg)

    # # 一条一条发送消息
    # for msg in get_msg():
    #     send(msg)
    #     # 每条消息间隔 2 秒
    #     time.sleep(2)
    
    pyautogui.press('esc')

if __name__ == '__main__':
    friend_name = "小朋友"
    send_msg(friend_name)
