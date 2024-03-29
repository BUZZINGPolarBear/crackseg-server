import math
import argparse
import cv2
import os

PIXEL_MAX_VALUE = 255

# 디렉토리 수정
PATH = os.getcwd()+'/crack_width_checker'
IMG_PATH = PATH+'/data/'
SAVE_DIR = PATH+'/results/'


class Lens:
    # 0.25, 0.4, 0.65, 1.2mm
    def __init__(self, distance=1000, fl=12, siah=6.287, srph=4050):
        self.FL = fl  # FL: focalLength
        self.WD = distance * 0.001  # WD: workingDistance 0.34
        self.SIAH = siah  # SIAH: sensorImageArea 14.0
        self.SRPH = srph  # SRPH: sensorResolßßßution 9248

        # if distance <= 2000 : distance += 1000

        self.PMAG = self.FL / (distance)  # PMAG
        self.HFOV = self.SIAH / self.PMAG  # HFOV
        self.SPP = self.HFOV / self.SRPH  # SPP: Size Per Pixel

        print("SPP(0.39):", self.SPP, ",  HFOV(1572):", self.HFOV, ", PMAG(0.004):", self.PMAG)
        self.R = 0.045 * ((self.WD) ** 2) - 0.355 * (self.WD) + 0.82  # 감소계수

    def real_width(self, pixel_width_list):
        real_width_list = [pixels * self.SPP * self.R for pixels in pixel_width_list]
        # [math.exp((pixel_num * SPP - (0.28 * WD) - 2.23) / 0.578) for pixel_num in pixel_num_list]
        return real_width_list

    def real_max_width(self, max_width_pixel):
        real_max_width = float(max_width_pixel) * self.SPP * self.R
        # [math.exp((pixel_num * SPP - (0.28 * WD) - 2.23) / 0.578) for pixel_num in pixel_num_list]
        return real_max_width

    def real_length(self, pixel_length_list):
        real_length_list = [pixels * self.SPP * self.R for pixels in pixel_length_list]
        return real_length_list


class Color:
    def __init__(self):
        (minN, midN, maxN) = (0, 150, 255)
        self.WIDEST_COLOR_P = [midN, midN, maxN]  # Pink
        self.WIDER_COLOR_Y = [minN, maxN, maxN]  # Yellow
        self.NORMAL_COLOR_G = [minN, midN, minN]  # Green
        self.LOWER_COLOR_B = [maxN, minN, minN]  # Blue
        self.LOWEST_COLOR_G = [midN, midN, midN]  # Gray
        self.ZERO_COLOR_B = [maxN, minN, minN]  # Gray
        self.first_lowest = self.second = self.third = self.fourth_highest = 0

    def dividing_3(self, total_LoW_list, mode='width'):
        if mode == 'width':
            sorted_set_list = list(set.union(*map(set, total_LoW_list)))
        else:
            sorted_set_list = list(set(total_LoW_list).union())

        num_divided_by_3 = round(len(sorted_set_list) / 3)
        # print(len(sorted_set_list),sorted_set_list)
        num_4th_highest = sorted_set_list[-1]
        num_3th = sorted_set_list[-1 * num_divided_by_3]
        num_2nd = sorted_set_list[-2 * num_divided_by_3]
        num_1st_lowest = sorted_set_list[0]

        return num_1st_lowest, num_2nd, num_3th, num_4th_highest

    def pick_color_paint(self, num_1st_lowest, num_2nd, num_3th, num_4th_highest, crack_width):
        if num_1st_lowest <= crack_width < num_2nd:
            match_color = self.NORMAL_COLOR_G
        elif num_2nd <= crack_width < num_3th:
            match_color = self.WIDER_COLOR_Y
        elif num_3th <= crack_width <= num_4th_highest:
            match_color = self.WIDEST_COLOR_P
        else:
            match_color = self.ZERO_COLOR_B
        return match_color

    def display_crack_color(self, img_thin, segment_list, pixel_list, mode='width', direction_key_list=[[0, 0, 'O']]):

        if mode == 'interval_point':
            for i, j, _ in direction_key_list:
                cv2.circle(img_thin, (j, i), 10, (0, 255, 0), thickness=3)

        # num_1st_lowest, num_2nd, num_3th, num_4th_highest = self.dividing_3(pixel_list, mode)
        num_1st_lowest, num_2nd, num_3th, num_4th_highest = (0, 4, 5, 60)

        total_segment_zip = zip(segment_list, pixel_list)

        for segment_block, crack in total_segment_zip:
            if mode == 'width':
                each_segment_block = zip(segment_block, crack)
                for [row, col], crack_width in each_segment_block:
                    img_thin[row, col] = self.pick_color_paint(num_1st_lowest, num_2nd, num_3th, num_4th_highest,
                                                               crack_width)
            else:
                for [row, col] in segment_block:
                    img_thin[row, col] = self.pick_color_paint(num_1st_lowest, num_2nd, num_3th, num_4th_highest, crack)

        return img_thin


'''
    def fill_crack_color_width(self, img, segment_list, pixel_list):

        num_1st_lowest, num_2nd, num_3th, num_4th_highest = (0, 4, 5, 60)
        total_segment_zip = zip(segment_list, pixel_list)

        for segment_block, crack in total_segment_zip:
            each_segment_block = zip(segment_block, crack)
            for [row, col], crack_width in each_segment_block:
                match_color = self.pick_color_paint(num_1st_lowest, num_2nd, num_3th, num_4th_highest, crack_width)

                img[row, col] = match_color

        return img'''