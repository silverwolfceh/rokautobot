import traceback

from filepath.constants import MAP
from filepath.file_relative_paths import BuffsImageAndProps, ItemsImageAndProps, ImagePathAndProps
from tasks.Task import Task
from tasks.constants import TaskName, Resource
import time

class GatherGem(Task):

    def __init__(self, bot):
        super().__init__(bot)
        self.max_query_space = 1

    def do(self, next_task=TaskName.BREAK):
        self.set_text(title='Thu thập Gem', remove=True)
        self.set_text(insert='Đang hoạt động')
        self.set_text(insert='Bản đồ thành phố')
        self.back_to_home_gui()
        self.set_text(insert='Bản đồ vương quốc')
        self.back_to_map_gui()
        try:
            if self.bot.config.aroundTroops:
                self.set_text(insert='kiểm tra chỉ huy quay lại khi khởi động')
                found, _, pos = self.gui.check_any(ImagePathAndProps.SCOUT_RETURN_ICON_IMAGE_PATH.value)
                if found:
                    self.check_return()
                    self.set_text(insert='có chỉ huy đang quay về,\n bắt đầu thu thập gem')
                    self.MoveSearchGem()
                    return next_task
                self.swipe(1225, 373, 1225, 234, 2)
                found, _, pos = self.gui.check_any(ImagePathAndProps.SCOUT_RETURN_ICON_IMAGE_PATH.value)
                if found:
                    self.check_return()
                    self.set_text(insert='có chỉ huy đang quay về,\n bắt đầu thu thập gem')
                    self.swipe(1225, 234, 1200, 373, 1)
                    self.MoveSearchGem()
                    return next_task
                self.swipe(1225, 234, 1200, 373, 1)
                self.set_text(insert='kiểm tra chỉ huy nhàn rỗi khi khởi động')
                found, _, pos = self.gui.check_any(ImagePathAndProps.HOLD_COM_ICON_IMAGE_PATH.value)
                if found:
                    self.check_idle()
                    self.set_text(insert='có một đội quân không hoạt động,\n bắt đầu thu thập gem')
                    self.MoveSearchGem()
                    return next_task
                self.swipe(1225, 373, 1225, 234, 2)
                is_found, _, pos_idle = self.gui.check_any(ImagePathAndProps.HOLD_COM_ICON_IMAGE_PATH.value)
                if is_found:
                    self.check_idle()
                    self.set_text(insert='có một đội quân không hoạt động,\n bắt đầu thu thập gem')
                    self.swipe(1225, 234, 1200, 373, 1)
                    self.MoveSearchGem()
                    return next_task
                self.swipe(1225, 234, 1200, 373, 1)
                self.input_coordinates()
                space = self.check_query_space()
                self.set_text(insert='kiểm tra quân số khi khởi động')
                if space > 0:
                    self.set_text(insert=('số lượng chỉ huy không hoạt động là {},\n Bắt đầu thu thập gem'.format(space)))
                    self.MoveSearchGem()
                    return next_task
                self.set_text(insert='Tất cả các chỉ huy đang bận, dừng thu thập gem')
                self.set_text(insert='kiểm tra có quân đội khi khởi động')
                found, _, pos = self.gui.check_any(ImagePathAndProps.HAS_MATCH_QUERY_IMAGE_PATH.value)
                if not found:
                    self.set_text(insert='không có quân đội nào đang thu thập,\n bắt đầu thu thập gem')
                    self.MoveSearchGem()
                    return next_task
            if self.bot.config.aroundCoor:
                self.input_coordinates()
                space = self.check_query_space()
                self.set_text(insert='kiểm tra quân số khi khởi động')
                if space > 0:
                    self.set_text(insert=('số lượng chỉ huy không hoạt động là {},\n Bắt đầu thu thập gem'.format(space)))
                    self.MoveSearchGem()
                    return next_task
                self.set_text(insert='Tất cả các chỉ huy đang bận, dừng thu thập gem')
                self.set_text(insert='kiểm tra có quân đội khi khởi động')
                found, _, pos = self.gui.check_any(ImagePathAndProps.HAS_MATCH_QUERY_IMAGE_PATH.value)
                if not found:
                    self.set_text(insert='không có quân đội nào đang thu thập,\n bắt đầu thu thập gem')
                    self.MoveSearchGem()
                    return next_task
                self.set_text(insert='kiểm tra chỉ huy đang quay về')
                found, _, pos = self.gui.check_any(ImagePathAndProps.SCOUT_RETURN_ICON_IMAGE_PATH.value)
                if found:
                    self.set_text(insert='có chỉ huy đang quay về, bắt đầu tìm kiếm')
                    self.MoveSearchGem()
                else:
                    self.swipe(1200, 350, 1200, 200, 2)
                    found, _, pos = self.gui.check_any(ImagePathAndProps.SCOUT_RETURN_ICON_IMAGE_PATH.value)
                    if found:
                        self.set_text(insert='có chỉ huy đang quay về, bắt đầu tìm kiếm')
                        self.swipe(1200, 200, 1200, 350, 1)
                        self.MoveSearchGem()
                    else:
                        self.set_text(insert='không có chỉ huy đang quay về, kết thúc')
                        self.swipe(1200, 200, 1200, 350, 1)
        except Exception as e:
            try:
                traceback.print_exc()
                return next_task
            finally:
                e = None
                del e

        return next_task

    def MoveSearchGem(self):
        for j in range(1):
            self.set_text(insert='zoom out')
            self.press_f1()
            for i in range(1):
                self.set_text(insert='up 1')
                self.swipe(640, 110, 640, 620, 1)
                if self.bot.config.aroundTroops:
                    self.Gem_All()
                if self.bot.config.aroundCoor:
                    self.Gem_All2()

            for i in range(1):
                self.set_text(insert='right 1')
                self.swipe(1000, 360, 100, 360, 1)
                if self.bot.config.aroundTroops:
                    self.Gem_All()
                if self.bot.config.aroundCoor:
                    self.Gem_All2()

            for i in range(2):
                self.set_text(insert=('down [{}]'.format(i + 1)))
                self.swipe(640, 600, 640, 60, 1)
                if self.bot.config.aroundTroops:
                    self.Gem_All()
                if self.bot.config.aroundCoor:
                    self.Gem_All2()

            self.check_zoom()
            for i in range(2):
                self.set_text(insert=('left [{}]'.format(i + 1)))
                self.swipe(250, 360, 1100, 360, 1)
                if self.bot.config.aroundTroops:
                    self.Gem_All()
                if self.bot.config.aroundCoor:
                    self.Gem_All2()

            self.check_zoom()
            for i in range(3):
                self.set_text(insert=('up [{}]'.format(i + 1)))
                self.swipe(640, 110, 640, 620, 1)
                if self.bot.config.aroundTroops:
                    self.Gem_All()
                if self.bot.config.aroundCoor:
                    self.Gem_All2()

            self.check_zoom()
            for i in range(3):
                self.set_text(insert=('right [{}]'.format(i + 1)))
                self.swipe(1000, 360, 100, 360, 1)
                if self.bot.config.aroundTroops:
                    self.Gem_All()
                if self.bot.config.aroundCoor:
                    self.Gem_All2()

            self.check_zoom()
            for i in range(4):
                self.set_text(insert=('down [{}]'.format(i + 1)))
                self.swipe(640, 600, 640, 60, 1)
                if self.bot.config.aroundTroops:
                    self.Gem_All()
                if self.bot.config.aroundCoor:
                    self.Gem_All2()

            self.check_zoom()
            for i in range(4):
                self.set_text(insert=('left [{}]'.format(i + 1)))
                self.swipe(250, 360, 1100, 360, 1)
                if self.bot.config.aroundTroops:
                    self.Gem_All()
                if self.bot.config.aroundCoor:
                    self.Gem_All2()

            self.check_zoom()
            for i in range(5):
                self.set_text(insert=('up [{}]'.format(i + 1)))
                self.swipe(640, 110, 640, 620, 1)
                if self.bot.config.aroundTroops:
                    self.Gem_All()
                if self.bot.config.aroundCoor:
                    self.Gem_All2()

            self.check_zoom()
            for i in range(5):
                self.set_text(insert=('right [{}]'.format(i + 1)))
                self.swipe(1000, 360, 100, 360, 1)
                if self.bot.config.aroundTroops:
                    self.Gem_All()
                if self.bot.config.aroundCoor:
                    self.Gem_All2()

            self.check_zoom()
            for i in range(6):
                self.set_text(insert=('down [{}]'.format(i + 1)))
                self.swipe(640, 600, 640, 60, 1)
                if self.bot.config.aroundTroops:
                    self.Gem_All()
                if self.bot.config.aroundCoor:
                    self.Gem_All2()

            self.check_zoom()
            for i in range(6):
                self.set_text(insert=('left [{}]'.format(i + 1)))
                self.swipe(250, 360, 1100, 360, 1)
                if self.bot.config.aroundTroops:
                    self.Gem_All()
                if self.bot.config.aroundCoor:
                    self.Gem_All2()

            self.check_zoom()
            for i in range(1):
                self.set_text(insert=('up [{}]'.format(i + 1)))
                self.swipe(640, 110, 640, 620, 1)
                self.do(self, next_task=(TaskName.BREAK))

    def Gem_All(self):
        self.back_to_map_gui()
        pos = self.gui.check_any(ImagePathAndProps.GEM_MINE_ICON_IMAGE_PATH.value, ImagePathAndProps.GEM_MINE_ICON1_IMAGE_PATH.value, ImagePathAndProps.GEM_MINE_ICON2_IMAGE_PATH.value, ImagePathAndProps.GEM_MINE_ICON3_IMAGE_PATH.value, ImagePathAndProps.GEM_MINE_ICON4_IMAGE_PATH.value)[2]
        if pos is None:
            self.set_text(insert='đang tìm kiếm ')
            return
        self.set_text(insert='a! thấy rồi!!!')
        pos_gem = pos
        self.tap(pos_gem[0], pos_gem[1], 1)
        self.tap(650, 330, 1)
        pos = self.gui.check_any(ImagePathAndProps.RESOURCE_GATHER_BUTTON_IMAGE_PATH.value)[2]
        if pos is None:
            self.set_text(insert='mỏ gem đã bị cướp,\n bạn có muốn tấn công chúng?')
            self.press_f1()
            return
        gather_btn_pos = pos
        self.tap(gather_btn_pos[0], gather_btn_pos[1], 3)
        found, name, pos = self.gui.check_any(ImagePathAndProps.HOLD_ICON_IMAGE_PATH.value, ImagePathAndProps.HOLD_ICON6_IMAGE_PATH.value, ImagePathAndProps.HOLD_ICON7_IMAGE_PATH.value, ImagePathAndProps.NEW_TROOPS_BUTTON_IMAGE_PATH.value)
        if found:
            x, y = pos
            self.tap(x, y, 1)
            found, name, pos = self.gui.check_any(ImagePathAndProps.MARCH_BAR_IMAGE_PATH.value)
            if found:
                self.set_text(insert='hành quân')
                x, y = pos
                self.tap(x, y, 1)
                self.set_text(insert='kiểm tra vật cản, đợi 10s')
                time.sleep(10)
                found, _, pos = self.gui.check_any(ImagePathAndProps.PASS_ICON_IMAGE_PATH.value, ImagePathAndProps.PASS_ICON2_IMAGE_PATH.value)
                if found:
                    self.set_text(insert='bị cản bởi đèo, quay lại vị trí cũ')
                    self.input_coordinates()
                    time.sleep(3)
                    self.MoveSearchGem()
                else:
                    self.set_text(insert='không có vật cản, tiếp tục')
                    self.check_return()
                    self.check_idle()
                    self.MoveSearchGem()
            else:
                if self.bot.config.gatherGemNoSecondaryCommander:
                    self.set_text(insert='Xóa chỉ huy phụ')
                    self.tap(473, 501, 0.5)
                self.swipe(630, 200, 740, 200, 1, 1000)
                self.tap(930, 616, 1)
                self.set_text(insert='Tạo một đội quân mới để thu thập gem')
                self.set_text(insert='kiểm tra vật cản, đợi 10s')
                time.sleep(10)
                found, _, pos = self.gui.check_any(ImagePathAndProps.PASS_ICON_IMAGE_PATH.value, ImagePathAndProps.PASS_ICON2_IMAGE_PATH.value)
                if found:
                    self.set_text(insert='bị cản bởi đèo, quay lại vị trí cũ')
                    self.input_coordinates()
                    time.sleep(3)
                    self.MoveSearchGem()
                else:
                    self.set_text(insert='không có vật cản, tiếp tục')
                    self.check_return()
                    self.check_idle()
                    self.MoveSearchGem()
        else:
            self.set_text(insert='không có chỉ huy nào nhàn rỗi')
            self.back()
            self.do(self, next_task=(TaskName.BREAK))

    def Gem_All2(self):
        self.back_to_map_gui()
        pos = self.gui.check_any(ImagePathAndProps.GEM_MINE_ICON_IMAGE_PATH.value, ImagePathAndProps.GEM_MINE_ICON1_IMAGE_PATH.value, ImagePathAndProps.GEM_MINE_ICON2_IMAGE_PATH.value, ImagePathAndProps.GEM_MINE_ICON3_IMAGE_PATH.value, ImagePathAndProps.GEM_MINE_ICON4_IMAGE_PATH.value)[2]
        if pos is None:
            self.set_text(insert='đang tìm kiếm ')
            return
        self.set_text(insert='a! thấy rồi!!!')
        pos_gem = pos
        self.tap(pos_gem[0], pos_gem[1], 1)
        self.tap(650, 330, 1)
        pos = self.gui.check_any(ImagePathAndProps.RESOURCE_GATHER_BUTTON_IMAGE_PATH.value)[2]
        if pos is None:
            self.set_text(insert='mỏ gem đã bị cướp,\n bạn có muốn tấn công chúng?')
            time.sleep(0)
            self.press_f1()
            return
        gather_btn_pos = pos
        self.tap(gather_btn_pos[0], gather_btn_pos[1], 3)
        found, name, pos = self.gui.check_any(ImagePathAndProps.SCOUT_RETURN_ICON_IMAGE_PATH.value, ImagePathAndProps.SCOUT_RETURN6_ICON_IMAGE_PATH.value, ImagePathAndProps.SCOUT_RETURN7_ICON_IMAGE_PATH.value, ImagePathAndProps.NEW_TROOPS_BUTTON_IMAGE_PATH.value)
        if found:
            x, y = pos
            self.tap(x, y, 1)
            found, name, pos = self.gui.check_any(ImagePathAndProps.MARCH_BAR_IMAGE_PATH.value)
            if found:
                self.set_text(insert='hành quân')
                x, y = pos
                self.tap(x, y, 1)
                self.set_text(insert='kiểm tra vật cản, đợi 10s')
                time.sleep(10)
                found, _, pos = self.gui.check_any(ImagePathAndProps.PASS_ICON_IMAGE_PATH.value, ImagePathAndProps.PASS_ICON2_IMAGE_PATH.value)
                if found:
                    self.set_text(insert='bị cản bởi đèo, quay lại vị trí cũ')
                    self.input_coordinates()
                    time.sleep(3)
                    self.MoveSearchGem()
                else:
                    self.set_text(insert='không có vật cản, tiếp tục')
                    self.MoveSearchGem()
            else:
                if self.bot.config.gatherGemNoSecondaryCommander:
                    self.set_text(insert='Xóa chỉ huy phụ')
                    self.tap(473, 501, 0.5)
                self.swipe(630, 200, 740, 200, 1, 1000)
                self.tap(930, 616, 1)
                self.set_text(insert='Tạo một đội quân mới để thu thập gem')
                self.set_text(insert='kiểm tra vật cản, đợi 10s')
                time.sleep(10)
                found, _, pos = self.gui.check_any(ImagePathAndProps.PASS_ICON_IMAGE_PATH.value, ImagePathAndProps.PASS_ICON2_IMAGE_PATH.value)
                if found:
                    self.set_text(insert='bị cản bởi đèo, quay lại vị trí cũ')
                    self.input_coordinates()
                    time.sleep(3)
                    self.MoveSearchGem()
                else:
                    self.set_text(insert='không có vật cản, tiếp tục')
                    self.MoveSearchGem()
        else:
            self.set_text(insert='không có chỉ huy nào nhàn rỗi')
            self.back()
            self.do(self, next_task=(TaskName.BREAK))

    def check_query_space(self):
        found, _, _ = self.gui.check_any(ImagePathAndProps.HAS_MATCH_QUERY_IMAGE_PATH.value)
        curr_q, max_q = self.gui.match_query_to_string()
        print(curr_q)
        print(max_q)
        if curr_q is None:
            return self.max_query_space
        return max_q - curr_q

    def input_coordinates(self):
        self.back_to_map_gui()
        self.set_text(insert='đến tọa độ đã cài đặt')
        self.tap(435, 15, 1)
        if self.bot.config.coordinatesGatherXEntry:
            self.set_text(insert='nhập tọa độ X')
            self.tap(624, 142, 1)
            self.input_text(self.bot.config.coordinatesGatherXEntry)
            self.tap(1194, 668, 1)
        if self.bot.config.coordinatesGatherYEntry:
            self.set_text(insert='nhập tọa độ Y')
            self.tap(786, 142, 1)
            self.input_text(self.bot.config.coordinatesGatherYEntry)
            self.tap(1194, 668, 1)
            self.tap(880, 140, 1)

    def check_pass(self):
        found, _, pos = self.gui.check_any(ImagePathAndProps.PASS_ICON_IMAGE_PATH.value)
        if found:
            self.input_coordinates()
# okay decompiling C:\Users\tvv1hc\pythoncode\bot\tasks\GatherGem.pyc
