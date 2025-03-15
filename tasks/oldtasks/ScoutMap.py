import traceback
import time

from filepath.file_relative_paths import ImagePathAndProps
from tasks.constants import TaskName, BuildingNames
from tasks.Task import Task


class ScoutMap(Task):
    def __init__(self, bot):
        super().__init__(bot)
        self.cave_done = []
        self.mapfile = "resource/map_%s.txt" % self.bot.config.scoutMaptype
        self.lastidx = 0
        # with open(self.mapfile) as file:
            # self.lines = [line.rstrip() for line in file]

    def input_coordinates(self, X, Y):
        self.back_to_map_gui()
        self.set_text(insert='Go to coordinate %s %s' % (X,Y))
        self.tap(435, 15, 1)
        self.tap(624, 142, 1)
        self.input_text(X)
        self.tap(1194, 668, 1)
        self.tap(786, 142, 1)
        self.input_text(Y)
        self.tap(1194, 668, 1)
        self.tap(880, 140, 1)

    def click_on_cave(self):
        self.tap(1280/2,720/2)

    def do(self, next_task=TaskName.BREAK):
        try:
            self.set_text(title='Cave list investigation')
            for i in range(self.lastidx, len(self.lines)):
                line = self.lines[i]
                self.back_to_home_gui()
                self.back_to_map_gui()
                cx, cy, ctype = line.split(",")
                self.set_text(insert = "Goto cave coord: {}:{}".format(cx, cy))
                self.input_coordinates(cx, cy)
                time.sleep(2)
                found, name, pos = self.gui.min_max_check(
                    ImagePathAndProps.CAVE_IMG_DAY_PATH.value,
                    ImagePathAndProps.CAVE_EXLAIM1_IMG_PATH.value,
                    ImagePathAndProps.CAVE_EXLAIM2_IMG_PATH.value,
                    ImagePathAndProps.CAVE_IMG_PATH.value
                )
                if found:
                    x, y = pos
                    self.tap(x, y, 2)
                else:
                    self.set_text(insert = "Can't found cave")
                    return next_task

                found, name, pos = self.gui.check_any(
                    ImagePathAndProps.INVESTIGATE_BUTTON_IMAGE_PATH.value,
                    ImagePathAndProps.GREAT_BUTTON_IMAGE_PATH.value
                )

                if found:
                    x, y = pos
                    self.tap(x, y, 2)
                else:
                    self.cave_done.append(line)
                    self.set_text(insert = "This cave already done")
                    continue

                if name == ImagePathAndProps.INVESTIGATE_BUTTON_IMAGE_PATH.value[5]:
                    while True:
                        found, name, pos = self.gui.check_any(
                            ImagePathAndProps.SCOUT_IDLE_ICON_IMAGE_PATH.value,
                            ImagePathAndProps.SCOUT_ZZ_ICON_IMAGE_PATH.value
                        )

                        if found:
                            x, y = pos
                            self.tap(x - 10, y - 10, 2)
                        else:
                            self.set_text(insert = "All scouters are busy")
                            self.lastidx = i
                            return next_task

                        found, name, pos = self.gui.check_any(
                            ImagePathAndProps.SCOUT_SEND_BUTTON_IMAGE_PATH.value,
                        )

                        if found:
                            x, y = pos
                            self.tap(x, y, 2)
                        else:
                            self.set_text(insert = "No scout send button")
                            self.lastidx = i
                            return next_task
                else:
                    self.set_text(insert = "No investigate button")
                    self.lastidx = i
                    return next_task
            return next_task
        except Exception as e:
            traceback.print_exc()
            return next_task