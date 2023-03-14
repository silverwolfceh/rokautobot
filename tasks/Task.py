from time import sleep, time
import win32gui, win32con
from bot_related.device_gui_detector import GuiName, GuiDetector
from bot_related.bot_config import TrainingAndUpgradeLevel, BotConfig
from bot_related import haoi, twocaptcha
from config import HAO_I, TWO_CAPTCHA
from filepath.file_relative_paths import ImagePathAndProps, BuffsImageAndProps, ItemsImageAndProps
from datetime import datetime
from utils import aircv_rectangle_to_box, stop_thread
from enum import Enum

import config
import traceback
import time


from filepath.constants import \
    RESOURCES, SPEEDUPS, BOOSTS, EQUIPMENT, OTHER, MAP, HOME


class Task:

    center = (640, 360)

    def __init__(self, bot):
        self.bot = bot
        self.device = bot.device
        self.gui = bot.gui

    def call_idle_back(self):
        self.set_text(insert='call back idle commander')
        self.back_to_map_gui()
        while True:
            _, _, commander_pos = self.gui.check_any(ImagePathAndProps.HOLD_ICON_SMALL_IMAGE_PATH.value)
            if commander_pos is not None:
                x, y = commander_pos
                self.tap(x - 10, y - 10, 2)
                x, y = self.center
                self.tap(x, y)
                self.tap(x, y, 1)
            else:
                return
            _, _, return_btn_pos = self.gui.check_any(ImagePathAndProps.RETURN_BUTTON_IMAGE_PATH.value)
            if return_btn_pos is not None:
                x, y = return_btn_pos
                self.tap(x, y, 1)
            else:
                return

    def heal_troops(self):
        return
        self.set_text(insert='Heal Troops')
        heal_button_pos = (960, 590)
        self.back_to_home_gui()
        self.home_gui_full_view()
        self.tap(self.bot.building_pos['hospital'][0], self.bot.building_pos['hospital'][1], 2)
        self.tap(285, 20, 0.5)
        _, _, heal_icon_pos = self.gui.check_any(ImagePathAndProps.HEAL_ICON_IMAGE_PATH.value)
        if heal_icon_pos is None:
            return
        self.tap(heal_icon_pos[0], heal_icon_pos[1], 2)
        self.tap(heal_button_pos[0], heal_button_pos[1], 2)
        self.tap(self.bot.building_pos['hospital'][0], self.bot.building_pos['hospital'][1], 2)
        self.tap(self.bot.building_pos['hospital'][0], self.bot.building_pos['hospital'][1], 2)

    # Home
    def back_to_home_gui(self):
        loop_count = 0
        gui_name = None
        while True:
            result = self.get_curr_gui_name()
            gui_name, info = ['UNKNOW', None] if result is None else result
            if gui_name == GuiName.HOME.name:
                break
            elif gui_name == GuiName.MAP.name:
                x_pos, y_pos = info
                self.tap(x_pos, y_pos)
            elif gui_name == GuiName.WINDOW.name:
                self.back(1)
            else:
                self.back(1)
            loop_count = loop_count + 1
            time.sleep(0.5)
        return loop_count

    def find_home(self):
        has_green_home, _, pos = self.gui.check_any(ImagePathAndProps.GREEN_HOME_BUTTON_IMG_PATH.value)
        if not has_green_home:
            return None
        x, y = pos
        self.tap(x, y, 2)

    def home_gui_full_view(self):
        self.tap(60, 540, 1)
        self.tap(1105, 200, 1)
        self.tap(1220, 35, 2)

    # Building Position
    def find_building_title(self):
        result = self.gui.has_image_props(ImagePathAndProps.BUILDING_TITLE_MARK_IMG_PATH.value)
        if result is None:
            return None
        x0, y0, x1, y1 = aircv_rectangle_to_box(result["rectangle"])
        return x0, y0, x1, y1

    # Menu
    def menu_should_open(self, should_open=False):
        # close menu if open
        path, size, box, threshold, least_diff, gui = ImagePathAndProps.MENU_BUTTON_IMAGE_PATH.value
        x0, y0, x1, y1 = box
        c_x, c_y = x0 + (x1 - x0) / 2, y0 + (y1 - y0) / 2
        is_open, _, _ = self.gui.check_any(ImagePathAndProps.MENU_OPENED_IMAGE_PATH.value)
        if should_open and not is_open:
            self.tap(c_x, c_y, 0.5)
        elif not should_open and is_open:
            self.tap(c_x, c_y, 0.5)

    # Map
    def back_to_map_gui(self):
        loop_count = 0
        gui_name = None
        while True:
            result = self.get_curr_gui_name()
            gui_name, pos = ['UNKNOW', None] if result is None else result
            if gui_name == GuiName.MAP.name:
                break
            elif gui_name == GuiName.HOME.name:
                x_pos, y_pos = pos
                self.tap(x_pos, y_pos)
            elif gui_name == GuiName.WINDOW.name:
                self.back(1)
            else:
                self.back(1)
            loop_count = loop_count + 1
            time.sleep(0.5)
        return loop_count

    def get_curr_gui_name(self):
        if not self.isRoKRunning():
            self.set_text(insert='game is not running, try to start game')
            self.set_text(insert='chờ 20s')
            self.runOfRoK()
            time.sleep(10)
            self.tap(640, 360, 1)
            time.sleep(10)
            start = time.time()
            end = start
            while end - start <= 300 and self.isRoKRunning():
                result = self.gui.get_curr_gui_name()
                if result is None:
                    time.sleep(5)
                    end = time.time()
                else:
                    break

        pos_list = None
        while True:
            result = self.gui.get_curr_gui_name()
            gui_name, pos = ['UNKNOW', None] if result is None else result
            if gui_name == GuiName.VERIFICATION_VERIFY.name:
                self.tap(pos[0], pos[1], 5)
                pos_list = self.pass_verification()
            # elif gui_name == GuiName.VERIFICATION_CLOSE_REFRESH_OK.name and pos_list is None:
            #     pos_list = self.pass_verification()
            else:
                return result

    def pass_verification(self):
        pos_list = None
        try:
            self.set_text(insert='pass verification')
            box = (437, 100, 842, 554)
            ok = [760, 586]
            img = self.gui.get_curr_device_screen_img()
            img = img.crop(box)
            if config.global_config.method == HAO_I:
                pos_list = haoi.solve_verification(img)
            elif config.global_config.method == TWO_CAPTCHA:
                pos_list = twocaptcha.solve_verification(img)

                if pos_list is None:
                    self.set_text(insert='giải capcha thất bại')
                    return
                    print(pos_list)
                    for pos in pos_list:
                        self.tap(440 + pos[0], 109 + pos[1], 1)

                    self.tap(760, 586, 1)
                    time.sleep(3)
                    found, _, pos = self.gui.check_any(ImagePathAndProps.VERIFICATION_OK_BUTTON_IMAGE_PATH.value)
                    if found:
                        self.set_text(insert='thất bại, giải lại')
                        self.pass_verification()
                else:
                    self.set_text(insert='giải capcha thành công')
        except Exception as e:
            try:
                self.tap(100, 100, 1)
                traceback.print_exc()
            finally:
                e = None
                del e

        return pos_list

    def check_capcha(self):
        pos_list = None
        found, _, pos = self.gui.check_any(ImagePathAndProps.VERIFICATION_VERIFY_TITLE_IMAGE_PATH.value)
        if found:
            self.tap(pos[0], pos[1] + 258, 1)
            time.sleep(5)
            self.pass_verification()
        found, _, pos = self.gui.check_any(ImagePathAndProps.VERIFICATION_VERIFY_BUTTON_IMAGE_PATH.value)
        if found:
            self.tap(pos[0], pos[1], 1)
            time.sleep(5)
            self.pass_verification()
    def has_buff(self, checking_location, buff_img_props):
        # Where to check
        if checking_location == HOME:
            self.back_to_home_gui()
        elif checking_location == MAP:
            self.back_to_map_gui()
        else:
            return False
        # Start Checking
        has, _, _ = self.gui.check_any(buff_img_props)
        return has

    def use_item(self, using_location, item_img_props_list):

        # Where to use the item
        if using_location == HOME:
            self.back_to_home_gui()
        elif using_location == MAP:
            self.back_to_map_gui()
        else:
            return False

        items_icon_pos = (930, 675)
        use_btn_pos = (980, 600)

        for item_img_props in item_img_props_list:
            path, size, box, threshold, least_diff, tab_name = item_img_props

            tabs_pos = {
                RESOURCES: (250, 80),
                SPEEDUPS: (435, 80),
                BOOSTS: (610, 80),
                EQUIPMENT: (790, 80),
                OTHER: (970, 80),
            }
            # open menu
            self.menu_should_open(True)
            # open items window
            x, y = items_icon_pos
            self.tap(x, y, 2)
            # tap on tab
            x, y = tabs_pos[tab_name]
            self.tap(x, y, 1)
            # find item, and tap it
            _, _, item_pos = self.gui.check_any(item_img_props)
            if item_pos is None:
                continue
            x, y = item_pos
            self.tap(x, y, 0.5)
            # tap on use Item
            x, y = use_btn_pos
            self.tap(x, y)
            return True
        return False

    # Action
    def back(self, sleep_time=0.5):
        cmd = 'input keyevent 4'
        self.device.shell(cmd)
        time.sleep(sleep_time)

    # duration is in milliseconds
    def swipe(self, x_f, y_f, x_t, y_t, times=1, duration=300):
        cmd = "input swipe {} {} {} {} {}".format(x_f, y_f, x_t, y_t, duration)
        for i in range(times):
            self.device.shell(cmd)
            time.sleep(duration / 1000 + 0.2)

    def swipe2(self, x_f, y_f, x_t, y_t, times=1, duration=300):
        cmd = 'input swipe {} {} {} {} {}'.format(x_f, y_f, x_t, y_t, duration)
        for i in range(times):
            self.device.shell(cmd)
            time.sleep(duration / 1000 + 0.2)

    def zoom(self, x_f, y_f, x_t, y_t, times=1, duration=300, zoom_type='out'):
        cmd_hold = 'input swipe {} {} {} {} {}'.format(x_t, y_t, x_t, y_t, duration + 50)
        if type == 'out':
            cmd_swipe = 'input swipe {} {} {} {} {}'.format(x_f, y_t, x_f, y_t, duration)
        else:
            cmd_swipe = 'input swipe {} {} {} {} {}'.format(x_t, y_t, x_f, y_f, duration)

        for i in range(times):
            self.device.shell(cmd_hold)
            self.device.shell(cmd_swipe)
            time.sleep(duration / 1000 + 0.5 + 0.2)

    def move(self, direction = "up"):
        cmd_hold = "input swipe 200 300 200 400 200"
        if direction == "down":
            cmd_hold = "input swipe 200 300 200 200 200"
        elif direction == "right":
            cmd_hold = "input swipe 200 300 100 300 200"
        elif direction == "left":
            cmd_hold = "input swipe 200 300 300 300 200"
        self.device.shell(cmd_hold)
        time.sleep(0.1)

    # long_press_duration is in milliseconds
    def tap(self, x, y, sleep_time=0.1, long_press_duration=-1):
        cmd = None
        if long_press_duration > -1:
            cmd = 'input swipe {} {} {} {} {}'.format(x, y, x, y, long_press_duration)
            sleep_time = long_press_duration / 1000 + 0.2
        else:
            cmd = 'input tap {} {}'.format(x, y)

        str = self.device.shell(cmd)
        time.sleep(sleep_time)


    # Input some value
    def input(self, val, sleep_time=0.1):
        cmd = 'input text {}'.format(val)
        str = self.device.shell(cmd)
        time.sleep(sleep_time)

    # edit by seashell-freya, github: https://github.com/seashell-freya
    def isRoKRunning(self):
        cmd1 = 'dumpsys window windows | grep mCurrentFocus'
        str1 = self.device.shell(cmd1)
        cmd2 = 'dumpsys window displays | grep -E "mCurrentFocus|mFocusedApp"'
        str2 = self.device.shell(cmd2)
        glbpc = str1.find('com.lilithgame.roc.gp/com.harry.engine.MainActivity')
        gmtpc = str1.find('com.rok.gp.vn/com.harry.engine.MainActivity')
        glbmb = str2.find('com.lilithgame.roc.gp/com.harry.engine.MainActivity')
        gmtmb = str2.find('com.rok.gp.vn/com.harry.engine.MainActivity')
        if glbpc != -1:
            return glbpc != -1
        if gmtpc != -1:
            return gmtpc != -1
        if glbmb != -1:
            return glbmb != -1
        if gmtmb != -1:
            return gmtmb != -1

    def runOfRoK(self):
        cmd1 = 'am start -n com.lilithgame.roc.gp/com.harry.engine.MainActivity'
        cmd2 = 'am start -n com.rok.gp.vn/com.harry.engine.MainActivity'
        str1 = self.device.shell(cmd1)
        str2 = self.device.shell(cmd2)

    def stopRok(self):
        cmd1 = 'am force-stop com.lilithgame.roc.gp'
        str1 = self.device.shell(cmd1)
        cmd2 = 'am force-stop com.rok.gp.vn'
        str2 = self.device.shell(cmd2)

    def set_text(self, **kwargs):
        dt_string = datetime.now().strftime("[%H:%M:%S]")
        title = 'title'
        text_list = 'text_list'
        insert = 'insert'
        remove = 'remove'
        replace = 'replace'
        index = 'index'
        append = 'append'

        if title in kwargs:
            self.bot.text[title] = kwargs[title]

        if replace in kwargs:
            self.bot.text[text_list][kwargs[index]] = dt_string + " " + kwargs[replace].lower()

        if insert in kwargs:
            self.bot.text[text_list].insert(kwargs.get(index, 0), dt_string + " " + kwargs[insert].lower())

        if append in kwargs:
            self.bot.text[text_list].append(dt_string + " " + kwargs[append].lower())

        if remove in kwargs and kwargs.get(remove, False):
            self.bot.text[text_list].clear()

        self.bot.text_update_event(self.bot.text)

    def do(self, next_task):
        return next_task
    def check_return(self):
        self.set_text(insert='kiểm tra chỉ huy đang quay về')
        found, _, pos = self.gui.check_any(ImagePathAndProps.SCOUT_RETURN_ICON_IMAGE_PATH.value)
        if found:
            self.tap(pos[0] - 10, pos[1] - 10, 2)
            found, _, pos = self.gui.check_any(ImagePathAndProps.HOLD_COM_BUTTON_IMAGE_PATH.value)
            self.tap(pos[0] - 10, pos[1] - 10, 2)
        else:
            self.swipe(1200, 350, 1200, 200, 1)
            found, _, pos = self.gui.check_any(ImagePathAndProps.SCOUT_RETURN_ICON_IMAGE_PATH.value)
            if found:
                self.tap(pos[0] - 10, pos[1] - 10, 2)
                found, _, pos = self.gui.check_any(ImagePathAndProps.HOLD_COM_BUTTON_IMAGE_PATH.value)
                self.tap(pos[0] - 10, pos[1] - 10, 2)
                self.swipe(1200, 200, 1200, 350, 1)
                return
            self.swipe(1200, 200, 1200, 350, 1)
    def check_idle(self):
        self.set_text(insert='kiểm tra chỉ huy rảnh rỗi')
        found, _, pos = self.gui.check_any(ImagePathAndProps.HOLD_COM_ICON_IMAGE_PATH.value)
        if found:
            self.set_text(insert='chọn chỉ huy nhàn rỗi')
            self.tap(pos[0] - 10, pos[1] - 10, 1)
        else:
            self.swipe(1200, 350, 1200, 200, 1)
            is_found, _, pos_idle = self.gui.check_any(ImagePathAndProps.HOLD_COM_ICON_IMAGE_PATH.value)
            if is_found:
                self.set_text(insert='chọn chỉ huy nhàn rỗi')
                x, y = pos_idle
                self.tap(x - 10, y - 10, 1)
                self.swipe(1200, 200, 1200, 350, 1)
            else:
                self.swipe(1200, 200, 1200, 350, 1)
    def march_gem(self):
        self.set_text(insert='hành quân')
        found, _, pos = self.gui.check_any(ImagePathAndProps.MARCH_BAR_IMAGE_PATH.value)
        if found:
            self.tap(pos[0], pos[1], 1)
    def input_text(self, keyboard):
        cmd = 'input text {}'.format(keyboard)
        self.device.shell(cmd)
    def check_zoom(self):
        found, _, pos = self.gui.check_any(ImagePathAndProps.MAGNIFIER_ICON_IMAGE_PATH.value)
        if found:
            self.press_f1()
    def press_f1(self):
        if self.bot.config.Gem1:

            def gem_handle(hwnd, none):
                print(win32gui.GetWindowText(hwnd))
                if self.bot.config.Gem1 in win32gui.GetWindowText(hwnd):
                    
                    win32gui.FindWindowEx(hwnd, None, None, 'MainWindowWindow')
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)

            win32gui.EnumWindows(gem_handle, None)
        if self.bot.config.Gem2:

            def gem_handle(hwnd, none):
                if self.bot.config.Gem2 in win32gui.GetWindowText(hwnd):
                    win32gui.FindWindowEx(hwnd, None, None, 'MainWindowWindow')
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)

            win32gui.EnumWindows(gem_handle, None)
        if self.bot.config.Gem3:

            def gem_handle(hwnd, none):
                if '(Gem3)' in win32gui.GetWindowText(hwnd):
                    win32gui.FindWindowEx(hwnd, None, None, 'MainWindowWindow')
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)

            win32gui.EnumWindows(gem_handle, None)
        if self.bot.config.Gem4:

            def gem_handle(hwnd, none):
                if '(Gem4)' in win32gui.GetWindowText(hwnd):
                    win32gui.FindWindowEx(hwnd, None, None, 'MainWindowWindow')
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)

            win32gui.EnumWindows(gem_handle, None)
        if self.bot.config.Gem5:

            def gem_handle(hwnd, none):
                if '(Gem5)' in win32gui.GetWindowText(hwnd):
                    win32gui.FindWindowEx(hwnd, None, None, 'MainWindowWindow')
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)

            win32gui.EnumWindows(gem_handle, None)
        if self.bot.config.Gem6:

            def gem_handle(hwnd, none):
                if '(Gem6)' in win32gui.GetWindowText(hwnd):
                    win32gui.FindWindowEx(hwnd, None, None, 'MainWindowWindow')
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)

            win32gui.EnumWindows(gem_handle, None)
        if self.bot.config.Gem7:

            def gem_handle(hwnd, none):
                if '(Gem7)' in win32gui.GetWindowText(hwnd):
                    win32gui.FindWindowEx(hwnd, None, None, 'MainWindowWindow')
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)

            win32gui.EnumWindows(gem_handle, None)
        if self.bot.config.Gem8:

            def gem_handle(hwnd, none):
                if '(Gem8)' in win32gui.GetWindowText(hwnd):
                    win32gui.FindWindowEx(hwnd, None, None, 'MainWindowWindow')
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)

            win32gui.EnumWindows(gem_handle, None)
        if self.bot.config.Gem9:

            def gem_handle(hwnd, none):
                if '(Gem9)' in win32gui.GetWindowText(hwnd):
                    win32gui.FindWindowEx(hwnd, None, None, 'MainWindowWindow')
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)

            win32gui.EnumWindows(gem_handle, None)
        if self.bot.config.Gem10:

            def gem_handle(hwnd, none):
                if '(Gem10)' in win32gui.GetWindowText(hwnd):
                    win32gui.FindWindowEx(hwnd, None, None, 'MainWindowWindow')
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)

            win32gui.EnumWindows(gem_handle, None)
        if self.bot.config.Gem11:

            def gem_handle(hwnd, none):
                if '(Gem11)' in win32gui.GetWindowText(hwnd):
                    win32gui.FindWindowEx(hwnd, None, None, 'MainWindowWindow')
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)

            win32gui.EnumWindows(gem_handle, None)
        if self.bot.config.Gem12:

            def gem_handle(hwnd, none):
                if '(Gem12)' in win32gui.GetWindowText(hwnd):
                    win32gui.FindWindowEx(hwnd, None, None, 'MainWindowWindow')
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)

            win32gui.EnumWindows(gem_handle, None)
        if self.bot.config.Gem13:

            def gem_handle(hwnd, none):
                if '(Gem13)' in win32gui.GetWindowText(hwnd):
                    win32gui.FindWindowEx(hwnd, None, None, 'MainWindowWindow')
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)

            win32gui.EnumWindows(gem_handle, None)
        if self.bot.config.Gem14:

            def gem_handle(hwnd, none):
                if '(Gem14)' in win32gui.GetWindowText(hwnd):
                    win32gui.FindWindowEx(hwnd, None, None, 'MainWindowWindow')
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)

            win32gui.EnumWindows(gem_handle, None)
        if self.bot.config.Gem15:

            def gem_handle(hwnd, none):
                if '(Gem15)' in win32gui.GetWindowText(hwnd):
                    win32gui.FindWindowEx(hwnd, None, None, 'MainWindowWindow')
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)

            win32gui.EnumWindows(gem_handle, None)
        if self.bot.config.Gem16:

            def gem_handle(hwnd, none):
                if '(Gem16)' in win32gui.GetWindowText(hwnd):
                    win32gui.FindWindowEx(hwnd, None, None, 'MainWindowWindow')
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F1)
                    sleep(4)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F1)

            win32gui.EnumWindows(gem_handle, None)
