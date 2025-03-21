from PIL import Image
from filepath.file_relative_paths import ImagePathAndProps
from filepath.file_relative_paths import GuiCheckImagePathAndPropsOrdered
from filepath.file_relative_paths import FilePaths
from utils import resource_path
from utils import img_to_string,img_to_string1
from utils import img_remove_background_and_enhance_word
from utils import bot_print

from enum import Enum
import traceback
import numpy as np
import cv2
from bot_related import aircve as aircv
import io


# small percentage are more similar
def cal_similarity(image1, image2):
    res = cv2.absdiff(image1, image2)
    # --- convert the result to integer type ---
    res = res.astype(np.uint8)
    # --- find percentage difference based on number of pixels that are not zero ---
    percentage = (np.count_nonzero(res) * 100) / res.size

    return percentage


class GuiName(Enum):
    HOME = 0
    MAP = 1
    WINDOW = 2
    WINDOW_TITLE = 3
    # VERIFICATION_CHEST = 4
    VERIFICATION_VERIFY = 5
    # VERIFICATION_VERIFY_TITLE = 6
    # VERIFICATION_CLOSE_REFRESH_OK = 7


class GuiDetector:

    def __init__(self, device):
        self.debug = False
        self.__device = device

    def get_curr_device_screen_img_byte_array(self):
        return self.__device.screencap()

    def get_curr_device_screen_img(self):
        return Image.open(io.BytesIO(self.__device.screencap()))

    def save_screen(self, file_name):
        image = Image.open(io.BytesIO(self.__device.screencap()))
        image.save(resource_path(FilePaths.TEST_SRC_FOLDER_PATH.value + file_name))

    def get_curr_gui_name(self):
        for image_path_and_props in GuiCheckImagePathAndPropsOrdered:
            result = self.check_any(image_path_and_props.value)
            if result[0]:
                return [result[1], result[2]]
        return None

    def get_windows_name(self):
        path, size, box, threshold, least_diff, gui = ImagePathAndProps.WINDOW_TITLE_MARK_IMG_PATH.value

        imsch = cv2.resize(
            cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8), cv2.IMREAD_COLOR),
            size
        )
        imsrc = cv2.imread(resource_path(path))

        # find 2 window title mark location
        result = aircv.find_all_template(imsrc, imsch, threshold)

        # get box position from result
        x0, x1, y0, y1 = 0, 0, 0, 0
        if result is not None and len(result) == 2:
            x0 = result[0]['rectangle'][2][0] + 50
            x1 = result[1]['rectangle'][0][0] - 50
            y0 = result[0]['rectangle'][0][1]
            y1 = result[0]['rectangle'][1][1]
        else:
            return None
        # crop image for ocr
        title_image = imsch[y0:y1, x0:x1]
        title_image = img_remove_background_and_enhance_word(title_image, np.array([0, 0, 160]),
                                                             np.array([255, 255, 255]))
        title_image = Image.fromarray(title_image)
        return img_to_string(title_image)

    def resource_amount_image_to_string(self):
        result_list = []
        # boxes = [
        #     (695, 10, 770, 34), (820, 10, 890, 34), (943, 10, 1015, 34), (1065, 10, 1140, 34)
        # ]
        boxes = [
            (690, 10, 765, 33), (814, 10, 883, 33), (934, 10, 1007, 33), (1058, 10, 1131, 33)
        ]
        for box in boxes:
            x0, y0, x1, y1 = box
            imsch = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8),
                                 cv2.IMREAD_COLOR)
            imsch = imsch[y0:y1, x0:x1]
            resource_image = Image.fromarray(imsch)
            try:
                octret = img_to_string(resource_image)
                hasprecison = octret.split(".")
                if len(hasprecison) == 2:
                    result_list.append(abs(int(octret
                                            .replace('.', '')
                                            .replace('B', '00000000')
                                            .replace('M', '00000')
                                            .replace('K', '00')
                                            ))
                                    )
                elif len(hasprecison) == 1:
                    result_list.append(abs(int(octret
                                            .replace('.', '')
                                            .replace('B', '000000000')
                                            .replace('M', '000000')
                                            .replace('K', '000')
                                            ))
                                    )

            except Exception as e:
                result_list.append(-1)
        return result_list

    def materilal_amount_image_to_string(self):
        result_list = []
        boxes = [
         (730, 243, 800, 264),
         (820, 245, 900, 264),
         (917, 245, 983, 264),
         (1000, 245, 1100, 264)]

        for box in boxes:
            x0, y0, x1, y1 = box
            imsch = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8),
                                 cv2.IMREAD_COLOR)
            imsch = cv2.cvtColor(imsch, cv2.COLOR_BGR2GRAY)
            imsch = imsch[y0:y1, x0:x1]
            ret, imsch = cv2.threshold(imsch, 215, 255, cv2.THRESH_BINARY)
            resource_image = Image.fromarray(imsch)
            try:
                result_list.append(int(img_to_string(resource_image)))
            except Exception as e:
                try:
                    result_list.append(-1)
                finally:
                    e = None
                    del e
        return result_list

    def resource_location_image_to_string(self):
        x0, y0, x1, y1 = (885, 190, 1035, 207)

        imsch = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8),
                             cv2.IMREAD_COLOR)
        imsch = cv2.cvtColor(imsch, cv2.COLOR_BGR2GRAY)
        imsch = imsch[y0:y1, x0:x1]
        ret, imsch = cv2.threshold(imsch, 215, 255, cv2.THRESH_BINARY)
        resource_image = Image.fromarray(imsch)
        result = ''.join(c for c in img_to_string(resource_image) if c.isdigit())
        return result

    def match_query_to_string(self):
        # x0, y0, x1, y1 = (1211, 162, 1242, 179)
        x0, y0, x1, y1 = (1200, 139, 1267, 155)

        try:
            imsch = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8),
                                 cv2.IMREAD_COLOR)
            imsch = cv2.cvtColor(imsch, cv2.COLOR_BGR2GRAY)
            imsch = imsch[y0:y1, x0:x1]
            cv2.imwrite('processed_image.png', imsch)
            ret, imsch = cv2.threshold(imsch, 215, 255, cv2.THRESH_BINARY)
            resource_image = Image.fromarray(imsch)
            ocrstring = img_to_string(resource_image)
            if len(ocrstring) == 3:
                if ocrstring[0].isdigit() and ocrstring[2].isdigit():
                    return (int(ocrstring[0]), int(ocrstring[2]))
            elif len(ocrstring) == 2:
                if ocrstring[0].isdigit() and ocrstring[1].isdigit():
                    return (int(ocrstring[0]), int(ocrstring[1]))
            return (None, None)
        except Exception as e:
            print(e)
            try:
                return (None, None)
            finally:
                e = None
                del e

    def barbarians_level_image_to_string(self):
        try:
            x0, y0, x1, y1 = (106, 370, 436, 384)
            imsch = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8),
                                 cv2.IMREAD_COLOR)
            imsch = cv2.cvtColor(imsch, cv2.COLOR_BGR2GRAY)
            imsch = imsch[y0:y1, x0:x1]
            # ret, imsch = cv2.threshold(imsch, 165, 255, cv2.THRESH_BINARY)
            resource_image = Image.fromarray(imsch)
            str = img_to_string(resource_image)
            if self.debug:
                cv2.imshow('imsch', imsch)
                print(str)
                cv2.waitKey(0)
            result = int(''.join(c for c in str if c.isdigit()))
        except Exception as e:
            try:
                traceback.print_exc()
                return -1
            finally:
                e = None
                del e
        if result > 99:
            return -1
        return result

    def get_building_name(self, box):
        x0, y0, x1, y1 = box
        title_image = self.get_curr_device_screen_img().crop(box)
        s = img_to_string(title_image)
        title_image.save(resource_path('{}title_x_{}_y_{}.png'.format(FilePaths.TEST_SRC_FOLDER_PATH.value, x0, y0)))
        bot_print("Building <{}> on position [({}, {}), ({}, {})] ".format(s, x0, y0, x1, y1))

    def check_any_cv2(self, *props_list):
        imsch = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8),
                             cv2.IMREAD_COLOR)
        grimsch = cv2.cvtColor(imsch, cv2.COLOR_BGR2GRAY)
        for props in props_list:
            path, size, box, threshold, least_diff, gui = props
            imsrc = cv2.imread(resource_path(path))
            grimsrc = cv2.cvtColor(imsrc, cv2.COLOR_BGR2GRAY)
            # cv2.imshow("dst", grimsrc)
            # cv2.imshow("src", grimsch)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            result = cv2.matchTemplate(grimsrc, grimsch, cv2.TM_CCOEFF_NORMED)
            # while True:
            #     loc = np.where(result >= threshold)
            #     if len(loc[0]) == 0:
            #         threshold = threshold - 0.05
            #     else:
            #         x, y = np.mean(loc[::-1], axis=1)
            #         return True, gui, (x,y)
            # _, max_val, _, max_loc = cv2.minMaxLoc(result)
            # return True, gui, max_loc
            loc = np.where(result >= threshold)
            if len(loc[0]) == 0:
                return False, None, None
            else:
                x, y = np.mean(loc[::-1], axis=1)
                return True, gui, (x,y)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)


    def min_max_check(self, *props_list):
        target = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8),
                             cv2.IMREAD_COLOR)
        for props in props_list:
            path, size, box, threshold, least_diff, gui = props
            # x0, y0, x1, y1 = box
            #if gui == 'NEW_TROOPS' or gui == 'CAVE_DAY':
            #self.save_screen(gui + ".png")
            template = cv2.imread(resource_path(path), cv2.IMREAD_COLOR)
            h, w = np.shape(template)[:2]

            result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
            # Locate the position of the template in the target image
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            print(min_loc, max_loc)
            
            result = (max_loc[0] + w/2, max_loc[1] + h/2)
            
            if self.debug:
                cv2.imshow('imsrc', target)
                cv2.imshow('imsch', template)
                cv2.waitKey(0)

            if result is not None:
                return True, gui, result

        return False, None, None

    def check_any(self, *props_list):
        imsch = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8),
                             cv2.IMREAD_COLOR)

        for props in props_list:
            path, size, box, threshold, least_diff, gui = props
            # x0, y0, x1, y1 = box
            #if gui == 'NEW_TROOPS' or gui == 'CAVE_DAY':
            #self.save_screen(gui + ".png")
            imsrc = cv2.imread(resource_path(path))

            result = aircv.find_template(imsrc, imsch, threshold, True)

            if self.debug:
                cv2.imshow('imsrc', imsrc)
                cv2.imshow('imsch', imsch)
                cv2.waitKey(0)

            if result is not None:
                return True, gui, result['result']

        return False, None, None

    def has_image_props(self, props):
        path, size, box, threshold, least_diff, gui = props
        imsch = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8),
                             cv2.IMREAD_COLOR)
        imsrc = cv2.imread(resource_path(path))
        result = aircv.find_template(imsrc, imsch, threshold, True)
        return result

    def find_all_image_props(self, props, max_cnt=3):
        path, size, box, threshold, least_diff, gui = props
        imsch = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8),
                             cv2.IMREAD_COLOR)
        imsrc = cv2.imread(resource_path(path))
        result = aircv.find_all_template(imsrc, imsch, threshold, max_cnt, True)
        return result

    def find_all_image_props2(self, props, max_cnt=3):
        path, size, box, threshold, least_diff, gui = props
        imsch = cv2.imdecode(np.asarray((self.get_curr_device_screen_img_byte_array()), dtype=(np.uint8)), cv2.IMREAD_COLOR)
        imsrc = cv2.imread(resource_path(path))
        result = aircv.find_all_template2(imsrc, imsch, threshold, max_cnt, True)
        return result
    def has_image_cv_img(self, cv_img, threshold=0.90):
        imsch = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8),
                             cv2.IMREAD_COLOR)
        result = aircv.find_template(cv_img, imsch, threshold, True)

        return result

    def get_image_in_box(self, box=(0, 0, 1280, 720)):
        """
        :param box: The crop rectangle, as a (left, upper, right, lower)-tuple.
        """
        x0, y0, x1, y1 = box
        img = cv2.imdecode(np.asarray(self.get_curr_device_screen_img_byte_array(), dtype=np.uint8),
                           cv2.IMREAD_COLOR)
        return img[y0:y1, x0:x1]
