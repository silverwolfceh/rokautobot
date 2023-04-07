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

    def do(self, next_task = TaskName.BREAK):
        found, name, pos = self.gui.check_any(ImagePathAndProps.NEW_TROOPS_BUTTON_IMAGE_PATH.value,
                                            ImagePathAndProps.NEW_TROOPS_BUTTON1_IMAGE_PATH.value,
                                            ImagePathAndProps.NEW_TROOPS_BUTTON2_IMAGE_PATH.value,
                                            ImagePathAndProps.NEW_TROOPS_BUTTON3_IMAGE_PATH.value,
                                            ImagePathAndProps.HOLD_ICON_IMAGE_PATH.value,
                                            ImagePathAndProps.HOLD_ICON6_IMAGE_PATH.value,
                                            ImagePathAndProps.HOLD_ICON7_IMAGE_PATH.value)
        if found:
            print("Test pass")
        else:
            print("Test failed")
        time.sleep(1000)
        self.set_text(title = 'Gem gathering', remove=True)
        self.set_text(insert = "Start gem gathering")
        if self.bot.config.gatherGemStartWithCord:
            self.back_to_home_gui()
            self.back_to_map_gui()
            self.set_text(insert = "Go to coordination {}-{}".format(self.bot.config.coordinatesGatherXEntry, self.bot.config.coordinatesGatherYEntry))
            self.input_coordinates()
        else:
            self.set_text(insert = "Start gather gem at current screen")

        try:
            space = self.check_query_space()
            if space > 0:
                self.set_text(insert = "Start gem farmining")
                #self.set_text(insert=('Số lượng chỉ huy không hoạt động là {},\n Bắt đầu thu thập gem'.format(space)))
                self.MoveSearchGem()
                return next_task
            found, _, pos = self.gui.check_any(ImagePathAndProps.HAS_MATCH_QUERY_IMAGE_PATH.value)
            if not found:
                self.set_text(insert = "Start gem farming 1")
                self.set_text(insert='không có quân đội nào đang thu thập,\n bắt đầu thu thập gem')
                self.MoveSearchGem()
                return next_task
            self.set_text(insert='kiểm tra chỉ huy đang quay về')
            found, _, pos = self.gui.check_any(ImagePathAndProps.SCOUT_RETURN_ICON_IMAGE_PATH.value)
            if found:
                self.set_text(insert='có chỉ huy đang quay về, bắt đầu tìm kiếm')
                self.MoveSearchGem()
                return next_task
            else:
                self.swipe(1200, 350, 1200, 200, 2)
                found, _, pos = self.gui.check_any(ImagePathAndProps.SCOUT_RETURN_ICON_IMAGE_PATH.value)
                if found:
                    self.set_text(insert='có chỉ huy đang quay về, bắt đầu tìm kiếm')
                    self.swipe(1200, 200, 1200, 350, 1)
                    self.MoveSearchGem()
                    return next_task
                else:
                    self.set_text(insert='không có chỉ huy đang quay về, kết thúc')
                    self.swipe(1200, 200, 1200, 350, 1)
            return next_task
        except Exception as e:
            try:
                traceback.print_exc()
                return next_task
            finally:
                e = None
                del e

        return next_task

    def move_to_direction(self, dir):
        if dir == "u":
            self.set_text(insert = "Move Up")
            self.swipe(640, 110, 640, 620, 1)
        elif dir == "d":
            self.set_text(insert = "Move Down")
            self.swipe(640, 600, 640, 60, 1)
        elif dir == "r":
            self.set_text(insert = "Move Right")
            self.swipe(1000, 360, 100, 360, 1)
        elif dir == "l":
            self.set_text(insert = "Move Left")
            self.swipe(250, 360, 1100, 360, 1)

    def MoveSearchGem(self):
        self.set_text(insert = "Bắt đầu zoom out bản đồ")
        self.zoom_out_using_f1()
        self.set_text(insert = "Bắt đầu tìm kiếm mỏ gem")
        time.sleep(2)
        self.Gem_All()
        x_width = 0
        y_width = 0
        #while x_width < self.bot.config.coordinateGatherXWidth:
        while True:
            if y_width >= int(self.bot.config.coordinateGatherYWidth):
                self.set_text(insert = "Xong một lượt")
                return
            # Move follow horizontal
            while y_width < int(self.bot.config.coordinateGatherYWidth):
                while x_width < int(self.bot.config.coordinateGatherXWidth):
                    if y_width % 2 == 0:
                        self.move_to_direction("r")
                    else:
                        self.move_to_direction("l")
                    x_width = x_width + 1
                    time.sleep(1)
                    self.Gem_All()
                x_width = 0
                y_width = y_width + 1
                self.move_to_direction("d")
                time.sleep(1)
                self.Gem_All()

    def find_all_possible_gem(self):
        #self.back_to_map_gui()
        pos = self.gui.check_any(ImagePathAndProps.GEM_MINE_ICON_IMAGE_PATH.value, 
                                 ImagePathAndProps.GEM_MINE_ICON1_IMAGE_PATH.value, 
                                 ImagePathAndProps.GEM_MINE_ICON2_IMAGE_PATH.value, 
                                 ImagePathAndProps.GEM_MINE_ICON3_IMAGE_PATH.value, 
                                 ImagePathAndProps.GEM_MINE_ICON4_IMAGE_PATH.value, 
                                 ImagePathAndProps.GEM_MINE_ICON5_IMAGE_PATH.value,
                                 ImagePathAndProps.GEM_MINE_ICON6_IMAGE_PATH.value,
                                 ImagePathAndProps.GEM_MINE_ICON7_IMAGE_PATH.value,
                                 ImagePathAndProps.GEM_MINE_ICON8_IMAGE_PATH.value,
                                 )[2]
        return pos

    def Gem_All(self):
        pos = self.find_all_possible_gem()
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
            self.zoom_out_using_f1()
            return
        gather_btn_pos = pos
        self.tap(gather_btn_pos[0], gather_btn_pos[1], 3)
        time.sleep(2)
        found, name, pos = self.gui.check_any(ImagePathAndProps.NEW_TROOPS_BUTTON_IMAGE_PATH.value,
                                            ImagePathAndProps.NEW_TROOPS_BUTTON1_IMAGE_PATH.value,
                                            ImagePathAndProps.NEW_TROOPS_BUTTON2_IMAGE_PATH.value,
                                            ImagePathAndProps.NEW_TROOPS_BUTTON3_IMAGE_PATH.value,
                                            ImagePathAndProps.HOLD_ICON_IMAGE_PATH.value,
                                            ImagePathAndProps.HOLD_ICON6_IMAGE_PATH.value,
                                            ImagePathAndProps.HOLD_ICON7_IMAGE_PATH.value)
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
                    self.set_text(insert='bị cản bởi đèo, bỏ qua')
                    #self.input_coordinates()
                    #time.sleep(3)
                    #self.MoveSearchGem()
                    return
                else:
                    self.set_text(insert='không có vật cản, tiếp tục')
                    self.check_return()
                    self.check_idle()
                    return
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
                    return
                    # self.input_coordinates()
                    # time.sleep(3)
                    # self.MoveSearchGem()
                else:
                    self.set_text(insert='không có vật cản, tiếp tục')
                    self.check_return()
                    self.check_idle()
                    return
        else:
            self.set_text(insert='không có chỉ huy nào nhàn rỗi')
            self.back()
            return

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
