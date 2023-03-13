import win32gui, win32con
import time
from time import sleep

def list_window(hdl, dataa):
    if 'memu' in win32gui.GetWindowText(hdl).lower():
        print(win32gui.GetWindowText(hdl).lower())
    if 'gem' in win32gui.GetWindowText(hdl).lower():
        print(win32gui.GetWindowText(hdl).lower())

def press_f1(hwnd, dataaa):
    if 'gem1' in win32gui.GetWindowText(hwnd).lower():
        win32gui.FindWindowEx(hwnd, None, None, 'MainWindowWindow')
        win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
        sleep(2)
        win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
        win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
        sleep(4)
        win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
        win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
        sleep(4)
        win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)


win32gui.EnumWindows(list_window, None)