import traceback

from filepath.file_relative_paths import ImagePathAndProps
from tasks.constants import BuildingNames
from tasks.constants import TaskName
from tasks.Task import Task
import time
import random


class RssTx(Task):
    def __init__(self, bot):
        super().__init__(bot)
        self.func_map = {
            "gold" : self.transfer_gold,
            "food" : self.transfer_food,
            "wood" : self.transfer_wood,
            "stone" : self.transfer_stone
        }
        self.rss = {"gold" : 3, "stone" : 2, "wood" : 1, "food" : 0}

    def log(self, msg):
        self.set_text(insert=msg)

    def go_to_coord(self):
            self.set_text(insert = "Go home")
            super().back_to_home_gui()
            self.set_text(insert = "To map")
            super().back_to_map_gui()
            X = int(self.bot.config.coordinatesTransXEntry)
            Y = int(self.bot.config.coordinatesTransYEntry)
            self.set_text(insert='Go to coordinate %s %s' % (X,Y))
            self.tap(435, 15, 1)
            self.tap(624, 142, 1)
            self.input_text(X)
            self.tap(1194, 668, 1)
            self.tap(786, 142, 1)
            self.input_text(Y)
            self.tap(1194, 668, 1)
            self.tap(880, 140, 1)
    
    def click_and_find_assit(self):
        self.tap(637, 320, 0.5)
        found, name, pos = self.gui.check_any(ImagePathAndProps.ASSIT_RESOURCE_IMAGE_PATH.value)
        if found:
            self.tap(pos[0], pos[1], 0.5)
            return True
        else:
            return False

    def check_transport_btn(self):
        found, name, pos = self.gui.check_any(ImagePathAndProps.TRANS_GRAY_IMAGE_PATH.value)
        return found

    def transfer_food(self):
        self.tap(591,222,0.1,1)
        self.swipe(591, 222, 888, 222, 1, 1000)

    def transfer_wood(self):
        self.tap(591,310,0.1,1)
        self.swipe(591, 310, 876, 314, 1, 500)

    def transfer_stone(self):
        self.tap(593,402,0.1,1)
        self.swipe(593, 402, 888, 407, 1, 500)
    
    def transfer_gold(self):
        self.tap(591,493,0.1,1)
        self.swipe(591, 493, 888, 493, 1, 500)

    def is_still_have_rss(self, rsstype):
        available_rss = self.gui.resource_amount_image_to_string()
        rssidx = self.rss[rsstype]
        if available_rss[rssidx] == -1:
            self.log("Failed to detect avail resource, ignore")
            return True
        elif available_rss[rssidx] < 3500000:
            self.log(f"No more {rsstype} to transfer {available_rss[rssidx]}")
            return False 
        else:
            return True

    def transport_rss(self, rsstype = "gold"):
        self.log(f"Start transport {rsstype}")
        while self.is_still_have_rss(rsstype):
            if self.is_map_gui():
                self.log("Click Assist")
                if self.click_and_find_assit():
                    time.sleep(0.5)
                    # self.gui.save_screen("abc.png")
                    if self.check_transport_btn():
                        self.log("Set max resource")
                        self.func_map[rsstype]()
                        self.log("Transport!")
                        while not self.press_transport():
                            self.log("Press transport failed, retry in 1 sec")
                            time.sleep(1)
                    else:
                        while not self.is_available_match():
                            self.log("No available match, sleep 3 seconds")
                            time.sleep(3)
                        self.log("Match available, continue")
                            
            else:
                self.log("Detect wrong map")
                break
        
        print("Here")
            

    def press_transport(self):
        found, name, pos = self.gui.check_any(ImagePathAndProps.TRANS_RESOURCE_IMAGE_PATH.value)
        if found:
            self.tap(pos[0], pos[1], 0.5)
            return True
        else:
            self.set_text(insert="Not found the transport button")
            return False

    def is_available_match(self):
        if self.is_map_gui() or self.is_home_gui():
            matches = self.gui.match_query_to_string()
            if matches[0] and matches[1]:
                return matches[0] < matches[1]
        else:
            self.back_to_map_gui()
        return False

    def do(self, next_task=TaskName.BREAK):
        super().set_text(title='RSS Transfer', remove=True)
        try:
            if self.is_available_match():
                self.go_to_coord()
                for k, v in self.rss.items():
                    self.transport_rss(k)
                return next_task
            else:
                self.log("Matches not available. Go to next task")
                return next_task
        except Exception as e:
            traceback.print_exc()
            return next_task