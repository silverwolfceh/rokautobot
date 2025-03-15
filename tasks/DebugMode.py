import traceback

from filepath.file_relative_paths import ImagePathAndProps
from tasks.constants import BuildingNames
from tasks.constants import TaskName
from tasks.Task import Task
import time
import random


class DebugMode(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def log(self, msg):
        self.set_text(insert=msg)

    def do(self, next_task=TaskName.BREAK):
        super().set_text(title='GOD Mode', remove=True)
        try:
            print(self.gui.resource_amount_image_to_string())
            time.sleep(10)
        except Exception as e:
            traceback.print_exc()
            return next_task