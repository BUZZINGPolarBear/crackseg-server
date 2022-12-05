import csv
import math
import time
import os.path
import cv2
import numpy as np
import params as pm
from skimage.morphology import medial_axis
from tqdm import tqdm

PIXEL_MAX_VALUE = 255

# 디렉토리 수정
PATH = os.getcwd()+'/crack_width_checker'
IMG_PATH = PATH+'/data/'
SAVE_DIR = PATH+'/results/'

MIN_CIRCULAR_MASK_RADIUS_RANGE = 7
MAX_CIRCULAR_MASK_RADIUS_RANGE = 50  # 원래 : 15

direction_set = ['N', 'NW', 'W', 'SW', 'S', 'SE', 'E', 'NE']
positive_table = direction_set[2:] + direction_set[:2]
p_c_table = direction_set[3:] + direction_set[:3]
p_f_table = direction_set[1:] + direction_set[:1]
# ['W', 'SW', 'S', 'SE', 'E', 'NE', 'N', 'NW']
negative_table = direction_set[6:] + direction_set[:6]
n_c_table = direction_set[7:] + direction_set[:7]  # 진행 방향의 가까이의 음의 수직
n_f_table = direction_set[5:] + direction_set[:5]  # 진행 방향의 멀리의  음의 수직
# ['E', 'NE', 'N', 'NW', 'W', 'SW', 'S', 'SE']
neighbor_key = ['NW', 'N', 'NE', 'E', 'SE', 'S', 'SW', 'W']

import params as pm

color = pm.Color()


def find_max(list):
    block_max = []
    for block in list:
        block_max.append(max(block))
    return (block_max)


def direction_dictionary(row, col):
    return {
        'NW': [row - 1, col - 1],
        'N': [row - 1, col],
        'NE': [row - 1, col + 1],
        'E': [row, col + 1],
        'SE': [row + 1, col + 1],
        'S': [row + 1, col],
        'SW': [row + 1, col - 1],
        'W': [row, col - 1]
    }


# 중심픽셀을 제외한 반지름이 7부터 15인 꽉찬 흰 원 만드는 함수
def circular_mask(radius):
    y, x = np.ogrid[-radius: radius + 1, -radius: radius + 1]
    mask = x ** 2 + y ** 2 <= radius ** 2
    mask = mask.astype(np.uint8)
    mask_area_pixel_num = np.count_nonzero(mask)

    return mask, mask_area_pixel_num


def masking_circular_area(img, row, col, radius, mask):
    crack_area_pixel_num = np.sum(
        np.multiply(mask, img[row - radius: row + radius + 1, col - radius: col + radius + 1]))
    crack_area_pixel_num /= PIXEL_MAX_VALUE

    return crack_area_pixel_num


def write_csv(rxw_item):
    file = SAVE_DIR + 'find_width_table.csv'

    if os.path.isfile(file):
        print("function : There is already a table to find crack width.", len(rxw_item))
    else:
        with open(SAVE_DIR + 'find_width_table.csv', 'w', newline='') as f:
            makewrite = csv.writer(f)
            for value in rxw_item:
                makewrite.writerow(value)


def read_csv():
    total_rxw_item_list = []

    with open(SAVE_DIR + 'find_width_table.csv', 'r') as f:
        reader = csv.reader(f)
        for raw_item_list in reader:
            int_item_list = [int(raw_item) for raw_item in raw_item_list]
            total_rxw_item_list.append(int_item_list)
    return total_rxw_item_list


def search_width_in_table(total_item_list, radius, crack_area_pixel_num):
    radius_index = radius - MIN_CIRCULAR_MASK_RADIUS_RANGE
    # print(radius_index, len(total_item_list))
    if radius_index >= len(total_item_list):
        return 0
    c = total_item_list[radius_index].copy()
    c.append(int(crack_area_pixel_num))
    d = sorted(c)
    crack_width = d.index(int(crack_area_pixel_num))

    return crack_width


# ac1에 있던 함수들 추가 -----------------------------------------------------

def closing_func(img):
    kernel = np.ones((19, 19), np.uint8)
    img_closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    result = cv2.subtract(img_closing, img)
    return result


def erode_func(img):
    kernel = np.ones((3, 3), np.uint8)
    img_closing = cv2.morphologyEx(img, cv2.MORPH_ERODE, kernel)
    result = cv2.subtract(img_closing, img)
    return result


def sharpening_func(img):
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    img = cv2.filter2D(img, -1, kernel)
    return img


def impacting_func(img, low=200, high=255):
    # int(input("최댓값 : "))
    height, width = img.shape
    for i in range(height):
        for a in range(width):
            if low <= img[i][a] <= high:
                img[i][a] = 255
    return img


def opening_func(img):
    kernel = np.ones((15, 15), np.uint8)
    img_opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    result = cv2.subtract(img_opening, img)
    return result


def opening_closing_func(img):
    # kernel = np.ones((3, 3), np.uint8)
    kernel, _ = circular_mask(1)
    img_opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    img_opening_closing = cv2.morphologyEx(img_opening, cv2.MORPH_CLOSE, kernel)
    return img_opening_closing


def closing_opening_func(img):
    # kernel = np.ones((3, 3), np.uint8)
    kernel, _ = circular_mask(1)
    img_closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    img_closing_opening = cv2.morphologyEx(img_closing, cv2.MORPH_OPEN, kernel)
    return img_closing_opening


def otsu_func(img):
    ret2, th2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print(ret2)
    return ret2, th2


def threshold_otsu_func(img, th):
    # ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_OTSU)
    # th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, blk_size, C)
    ret2, th2 = cv2.threshold(img, th, 255, cv2.THRESH_BINARY)
    print(ret2)
    return ret2, th2


def adaptive_gaussian_otsu_func(img):
    blk_size = 9  # 블럭 사이즈
    C = 5  # 차감 상수
    th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, blk_size, C)
    return th3


def noise_reduction_func(img, kernel_r=3, threshold=220):
    kernel = np.ones((kernel_r, kernel_r), np.float32) / (kernel_r ** 2)
    averaged_img = cv2.filter2D(img, -1, kernel)
    averaged_img[averaged_img < threshold] = 0
    averaged_img[averaged_img >= threshold] = 255

    return averaged_img


def circle_noise_removal_using_packing_density_func(img):
    from math import pi
    threshold = 0.1  # 0.12
    nlabels, img_labeled, stats, centroids = cv2.connectedComponentsWithStats(img, connectivity=8)

    for i in range(nlabels):
        if i < 1: continue  # 첫번째 노이즈가 자꾸 무시되어서 2를 1로 바꿔주었다.

        area = stats[i, cv2.CC_STAT_AREA]
        center_x = centroids[i, 0]
        center_y = centroids[i, 1]
        left = stats[i, cv2.CC_STAT_LEFT]
        top = stats[i, cv2.CC_STAT_TOP]
        width = stats[i, cv2.CC_STAT_WIDTH]
        height = stats[i, cv2.CC_STAT_HEIGHT]

        r = (width ** 2 + height ** 2) ** 0.5 / 2
        circle_area = pi * r * r
        key = area / circle_area

        if key > threshold: img[top: top + height, left: left + width] = 0
    return img


def combine_mask(img, mask):
    if img.shape != mask.shape:
        print(img.shape, mask.shape)
    if type(img) != type(mask):
        print(type(img), type(mask))
    return cv2.bitwise_and(img, mask)


def thinning_func(img):
    # Compute the medial axis (skeleton) and the distance transform
    skel, distance = medial_axis(img, return_distance=True)
    # Distance to the background for pixels of the skeleton
    dist_on_skel = (distance * skel).astype(np.uint8)
    dist_on_skel[dist_on_skel != 0] = 255
    return dist_on_skel


def boundary_func(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    # blank_image = np.zeros((734, 980, 1), np.uint8)
    blank_image = np.zeros((img.shape[0], img.shape[1], 1), np.uint8)

    for i in range(len(contours)):
        cv2.drawContours(blank_image, [contours[i]], 0, (255, 255, 255), 1)
    return blank_image


def search_start_interval_point_direction_key(img):
    start_interval_point_direction_key_list = []
    # 몇번째 위치를 접근하고 있는 지를 알려주는 표시

    # 시작점을 구하려면 주변의 색과 비교해야 해서, 테두리 1픽셀을 검게 칠해진 이미지 불러옴
    for row in range(1, img.shape[0] - 1):
        for col in range(1, img.shape[1] - 1):
            if img[row, col] == 255:
                pixel_dict = {
                    'NW': img[row - 1, col - 1],
                    'N': img[row - 1, col],
                    'NE': img[row - 1, col + 1],
                    'E': img[row, col + 1],
                    'SE': img[row + 1, col + 1],
                    'S': img[row + 1, col],
                    'SW': img[row + 1, col - 1],
                    'W': img[row, col - 1]
                }
                flag = 0
                for i in range(-8, 0):  # 'NW'부터 다음 픽셀과 색 비교
                    if int(pixel_dict[neighbor_key[i]]) - int(pixel_dict[neighbor_key[i + 1]]) == 255:
                        flag += 1

                # 분기점(특징점)일때 점과 주변 흰색 점의 방향들을 리스트 start_interval_point_direction_key_list에 추가
                if flag == 1 or flag >= 3:
                    for key in neighbor_key:
                        if pixel_dict[key] == 255:
                            start_interval_point_direction_key_list.append([row, col, key])

    return start_interval_point_direction_key_list


def display_start_interval_point(img, start_interval_point_direction_key_list):
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    for i, j, _ in start_interval_point_direction_key_list:
        cv2.circle(img, (j, i), 10, (0, 255, 0), thickness=3)
    cv2.imshow('hi', img)
    cv2.waitKey()

    return img


def search_edge_segment(img, start_interval_point_direction_key_list):
    total_segment_list = []
    total_chain_list = []

    # 특징점의 좌표[row,col]만 뽑아냄 (중복되는 좌표가 연속으로 존재할 수 있음)
    start_interval_point_list = list(map(lambda x: x[:2], start_interval_point_direction_key_list))
    # pdb.set_trace()

    # visited_map : [0]를 원소로 가지는 2차원 매트릭스(x*y)
    visited_map = np.zeros((img.shape[0], img.shape[1], 1), np.uint8)

    # tqdm: 진행상황 표시
    for row, col, key in tqdm(start_interval_point_direction_key_list):
        # pdb.set_trace()
        direction_dict = direction_dictionary(row, col)

        # 원소: (특징점 좌표, 이웃 좌표)
        segment_code = []

        # 원소: (특징점 좌표, 이웃 방향)
        chain_code = []

        # 방문한 좌표라면, 다음 (특징점,방향)원소로 접근
        if visited_map[tuple(direction_dict[key])] == 1:
            continue

        # 처음 방문한 좌표라면
        else:
            segment_code.extend([[row, col], direction_dict[key]])
            chain_code.extend([[row, col], key])
            visited_map[row, col] = 1  # 방명록에 특징점 좌표 작성
            visited_map[tuple(direction_dict[key])] = 1  # 방명록에 이웃 좌표 작성
            possible_key = ''
            # pdb.set_trace()

            if direction_dict[key] in start_interval_point_list:
                total_segment_list.append(segment_code)
                total_chain_list.append(chain_code)
                continue

            else:
                while True:
                    # pdb.set_trace()
                    row, col = direction_dict[key]

                    direction_dict = direction_dictionary(row, col)

                    if key == 'NW':
                        possible_key = ['SW', 'W', 'NW', 'N', 'NE']
                    elif key == 'N':
                        possible_key = ['NW', 'N', 'NE']
                    elif key == 'NE':
                        possible_key = ['NW', 'N', 'NE', 'E', 'SE']
                    elif key == 'E':
                        possible_key = ['NE', 'E', 'SE']
                    elif key == 'SE':
                        possible_key = ['NE', 'E', 'SE', 'S', 'SW']
                    elif key == 'S':
                        possible_key = ['SE', 'S', 'SW']
                    elif key == 'SW':
                        possible_key = ['SE', 'S', 'SW', 'W', 'NW']
                    elif key == 'W':
                        possible_key = ['SW', 'W', 'NW']
                    # pdb.set_trace()
                    end_point = [next_key for next_key in possible_key if
                                 direction_dict[next_key] in start_interval_point_list]
                    # pdb.set_trace()
                    if end_point:
                        for next_key in end_point:
                            segment_code.append(direction_dict[next_key])
                            chain_code.append(next_key)
                            visited_map[tuple(direction_dict[next_key])] = 1
                            total_segment_list.append(segment_code)
                            total_chain_list.append(chain_code)
                        break
                    else:
                        # print(row, col, possible_key, len(possible_key), img.shape)
                        next_point = [next_key for next_key in possible_key if
                                      img[tuple(direction_dict[next_key])] == 255]
                        # if end_point:
                        #    print(row, col)
                        if len(next_point) > 1:
                            # pdb.set_trace()
                            continue
                        for next_key in next_point:
                            segment_code.append(direction_dict[next_key])
                            chain_code.append(next_key)
                            visited_map[tuple(direction_dict[next_key])] = 1
                            key = next_key

    return total_segment_list, total_chain_list


def display_edge_segment(img, total_segment_list):
    cv2.imshow('hi', img)
    cv2.waitKey()

    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    for i, block in enumerate(total_segment_list, 1):
        for [row, col] in block:
            img[row, col] = [0, 0, 255]

    cv2.imshow('hi', img)
    cv2.waitKey()

    return img


def crack_length_func(total_chain_list):
    total_length_list = []
    for chain_block in total_chain_list:
        crack_length = 0
        for code in chain_block:
            if code == 'N' or code == 'E' or code == 'S' or code == 'W':
                crack_length += 1
            elif code == 'NW' or code == 'NE' or code == 'SE' or code == 'SW':
                crack_length += 2 ** 0.5
        total_length_list.append(crack_length)
    return total_length_list


def direction_func(direction, LorR=-1):
    # print(direction)
    d = direction_set.index(direction)
    positive_d = positive_table[d]
    negative_d = negative_table[d]
    p_c = p_c_table[d]  # type: ignore
    p_f = p_f_table[d]
    n_c = n_c_table[d]
    n_f = n_f_table[d]

    if LorR == 0:
        return positive_d, p_c, p_f
    elif LorR == 1:
        return negative_d, n_c, n_f
    else:
        return positive_d, negative_d, p_c, p_f, n_c, n_f


# 한 방향으로 연속되는 흰색 픽셀 수 구하기
def fill_color_until_black(img_BGR, img, img_th, start, direction, LorR=0, clr=[0, 0, 0]):
    row, col = (start[0], start[1])
    d_next, d_next_cl, d_next_fr = direction_func(direction, LorR=LorR)  # type: ignore

    while True:
        img_BGR[row, col] = clr
        direction_dict = direction_dictionary(row, col)
        next = direction_dict[d_next]  # 정중앙의 수직방향 다음 픽셀
        # next_c = direction_dict[d_next_cl]  # 가까이의 수직방향 다음 픽셀
        # next_f = direction_dict[d_next_fr]  # 더멀리의 수직방향 다음 픽셀

        # 0: 선분 진행 방향의 수직 균열 밖이면! : 검은색 픽셀이면
        if img[next[0], next[1]] != 255: break
        # if img[next_c[0], next_c[1]] != 255: break
        # if img[next_f[0], next_f[1]] != 255: break

        # 1-0: 선분 진행 방향의 수직 균열 내부라면! (흰색 픽셀) : 다른 균열의 중심부일 때! - 너비 끝
        if img_th[next[0], next[1]] == 255: break
        # if img_th[next_c[0], next_c[1]] != 0: break
        # if img_th[next_f[0], next_f[1]] != 0: break

        row, col = (next[0], next[1])
    # while 끝!!
    return img_BGR


# 한 방향으로 연속되는 흰색 픽셀 수 구하기
def finding_white_until_black(img, img_th, start, direction, LorR=0):
    width = 0
    row, col = (start[0], start[1])
    d_next, d_next_cl, d_next_fr = direction_func(direction, LorR=LorR)  # type: ignore

    while True:
        direction_dict = direction_dictionary(row, col)
        next = direction_dict[d_next]  # 정중앙의 수직방향 다음 픽셀
        next_c = direction_dict[d_next_cl]  # 가까이의 수직방향 다음 픽셀
        next_f = direction_dict[d_next_fr]  # 더멀리의 수직방향 다음 픽셀

        # 0: 선분 진행 방향의 수직 균열 밖이면! : 검은색 픽셀이면
        if img[next[0], next[1]] != 255: break
        if img[next_c[0], next_c[1]] != 255: break
        if img[next_f[0], next_f[1]] != 255: break

        # 1-0: 선분 진행 방향의 수직 균열 내부라면! (흰색 픽셀) : 다른 균열의 중심부일 때! - 너비 끝
        if img_th[next[0], next[1]] == 255: break
        if img_th[next_c[0], next_c[1]] != 0: break
        if img_th[next_f[0], next_f[1]] != 0: break

        width += 1
        row = next[0]
        col = next[1]
    # while 끝!!
    return width


# 너비 색상 표시 기법
def fill_crack_width_func(img, img_th, total_segment_list, total_chain_list, total_width_list):
    img_BGR = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    num_1st_lowest, num_2nd, num_3th, num_4th_highest = (0, 4, 5, 60)

    for j in range(len(total_width_list)):
        segment_block = total_chain_list[j]
        center_pixel_block = total_segment_list[j]
        width_block = total_width_list[j]
        for i in range(len(segment_block)):
            if len(segment_block) != len(width_block):
                print(len(segment_block), len(width_block), segment_block, width_block)
                break
            start = center_pixel_block[i - 1]
            if i == 0:
                direc = segment_block[1]
            else:
                direc = segment_block[i]
            width = width_block[i]
            clr = color.pick_color_paint(num_1st_lowest, num_2nd, num_3th, num_4th_highest, width)
            # left : 진행 방향 기준 왼쪽 수직 방향
            img_BGR = fill_color_until_black(img_BGR, img, img_th, start, direc, LorR=0, clr=clr)
            # right : 진행 방향 기준 오른쪽 수직 방향
            img_BGR = fill_color_until_black(img_BGR, img, img_th, start, direc, LorR=1, clr=clr)
        #
    #
    return img_BGR


# 추가된 너비 측정 방식 re
def renewal_profiling_crack_width_func(img, img_th, total_segment_list, total_chain_list):
    max_width = 23  # 20>1.3194938271604937, 23>1.5174179012345677
    total_width_list = []
    for j in range(len(total_chain_list)):
        segment_block = total_chain_list[j]
        center_pixel_block = total_segment_list[j]
        segment_width_block = []
        for i in range(0, len(segment_block)):
            start = center_pixel_block[i - 1]
            if i == 0:
                direc = segment_block[1]
            else:
                direc = segment_block[i]
            # left : 진행 방향 기준 왼쪽 수직 방향
            left_width = finding_white_until_black(img, img_th, start, direc, LorR=0)
            # right : 진행 방향 기준 오른쪽 수직 방향
            right_width = finding_white_until_black(img, img_th, start, direc, LorR=1)
            total_width = left_width + right_width - 1
            segment_width_block.append(max(total_width, 1))  # min(total_width, max_width)

        #
        total_width_list.append(segment_width_block)
    #
    return total_width_list, img


# 추가된 너비 측정 방식 0 - new one
def profiling_crack_width_func_new(img, img_th, total_chain_list):
    total_width_list = []

    for segment_block in total_chain_list:
        segment_width_block = []
        for i in range(1, len(segment_block)):
            start = segment_block[0]
            direc = segment_block[i]
            # left : 진행 방향 기준 왼쪽 수직 방향
            left_width = finding_white_until_black(img, img_th, start, direc, LorR=0)
            # right : 진행 방향 기준 오른쪽 수직 방향
            right_width = finding_white_until_black(img, img_th, start, direc, LorR=1)

            segment_width_block.append(left_width + right_width)

        #
        total_width_list.append(segment_width_block)
    #
    return total_width_list, img


# 추가된 너비 측정 방식 1 - old one
def profiling_crack_width_func(img, img_th, total_chain_list):
    p_list = []
    max_p = 0
    img_bgr = cv2.cvtColor(img_th, cv2.COLOR_GRAY2BGR)

    for segment_block in total_chain_list:
        temporary_list_segment_block = []
        if len(segment_block) > 7:
            for i in range(1, len(segment_block)):
                p_width = n_width = 0
                start = segment_block[0]
                positive_d, negative_d, pc, pf, nc, nf = direction_func(direction=segment_block[i],
                                                                        LorR=-1)  # type: ignore
                row = start[0]
                col = start[1]
                # img_bgr = cv2.circle(img_bgr, (col, row), 5, (0,0,255), 2)

                # 진행 방향 기준 왼쪽 수직 방향 : 양의 방향으로의 너비...
                while True:
                    direction_dict = direction_dictionary(row, col)
                    p_next_pixel = direction_dict[positive_d]
                    p_c = direction_dict[pc]  # 가까이의 양의 수직
                    p_f = direction_dict[pf]  # 멀리의  양의 수직
                    n_next_pixel = direction_dict[negative_d]
                    n_c = direction_dict[nc]
                    n_f = direction_dict[nf]

                    # 선분 진행 방향의 수직 중 음의 방향으로 나아갈 때, 균열 내부라면!
                    if img[n_next_pixel[0], n_next_pixel[1]] == 255:
                        # if img_th[p_c[0], p_c[1]] == 255 | img_th[p_f[0], p_f[1]] == 255 : break

                        # (음의) 수직 방향으로 균열(의 중심부) 아닐 때
                        if img_th[n_c[0], n_c[1]] == 255 | img_th[n_f[0], n_f[1]] == 255 | img_th[
                            n_next_pixel[0], n_next_pixel[1]] == 255:
                            break
                        elif img_th[n_next_pixel[0], n_next_pixel[1]] != 255:
                            p_width += 1
                            img_bgr[row, col] = (0, 255, 0)
                            # img_bgr = cv2.circle(img_bgr, (col, row), 3, (0,0,255), 1)
                            # img_bgr[n_next_pixel[0], n_next_pixel[1]] = [0,0,255]
                    else:
                        break
                    if p_width > 20:
                        img_bgr = cv2.circle(img_bgr, (col, row), 5, (255, 0, 0), 1)
                        img_bgr = cv2.circle(img_bgr, (start[1], start[0]), 5, (255, 255, 0), 1)
                    row = n_next_pixel[0]
                    col = n_next_pixel[1]

                temporary_list_segment_block.append(p_width)
                if max_p < p_width:
                    max_p = p_width
        temporary_list_segment_block.append(0)
        p_list.append(temporary_list_segment_block)

    return p_list, img_bgr


def adaptive_crack_width_func(img, total_segment_list):
    total_rxw_item_list = read_csv()
    total_width_list = []
    mask_list = []
    mask_area_pixel_num_list = []
    for radius in range(MIN_CIRCULAR_MASK_RADIUS_RANGE, MAX_CIRCULAR_MASK_RADIUS_RANGE):
        mask, mask_area_pixel_num = circular_mask(radius)
        mask_list.append(mask)
        mask_area_pixel_num_list.append(mask_area_pixel_num)
    circular_mask_cache_zip_list = list(
        zip(range(MIN_CIRCULAR_MASK_RADIUS_RANGE, MAX_CIRCULAR_MASK_RADIUS_RANGE), mask_list, mask_area_pixel_num_list))

    for segment_block in total_segment_list:
        width_list = []
        len_seg = len(segment_block)
        visit_list = np.zeros(len_seg)
        visit_idx = 0
        try_idx = 0
        for row, col in segment_block:
            # if try_idx != visit_idx :
            #     print(try_idx, visit_idx, visit_list)
            try:
                tempRadius = tempRatio = tempArea = 0
                crack_width = -2
                for radius, mask, mask_area_pixel_num in circular_mask_cache_zip_list:
                    crack_area_pixel_num = masking_circular_area(img, row, col, radius, mask)
                    if crack_area_pixel_num < mask_area_pixel_num / 2:
                        currntRatio = crack_area_pixel_num / mask_area_pixel_num
                        if abs(tempRatio - 0.5) < abs(currntRatio - 0.5):
                            crack_width = search_width_in_table(total_rxw_item_list, tempRadius, tempArea)
                        else:
                            crack_width = search_width_in_table(total_rxw_item_list, radius, crack_area_pixel_num)
                        break
                    tempRadius = radius
                    tempArea = crack_area_pixel_num
                    tempRatio = crack_area_pixel_num / mask_area_pixel_num
                width_list.append(crack_width)
                visit_list[try_idx] = 1
                try_idx += 1
            except ValueError:
                # 이미지의 4방면의 끝은 원 마스크의 인덱스를 적용하지 못하기 때문에, 연산 불가 에러가 나왔으며, 이경우 너비 구하기를 포기하고 너비를 0으로 선언한다.
                err = "error"
                # print(err)#,width_list)
            visit_idx += 1
            if try_idx < visit_idx:
                width_list.append(1)
                visit_list[try_idx] = 1
                # print(try_idx, visit_idx, visit_list[try_idx], width_list[try_idx], width_list)
                try_idx += 1
            #
        #
        if len(segment_block) != len(width_list):
            print(len(segment_block), len(width_list))
        total_width_list.append(width_list)

    return total_width_list


def normal_crack_width_func(img, total_segment_list, radius=20):
    total_rxw_item_list = read_csv()
    total_width_list = []
    mask, mask_area_pixel_num = circular_mask(radius)

    for segment_block in total_segment_list:
        width_list = []
        for row, col in segment_block:

            if row - radius < 0 or row + radius > img.shape[0] - 1 or col - radius < 0 or col + radius > img.shape[
                1] - 1:
                width_list.append(0)
                continue
            else:
                crack_area_pixel_num = masking_circular_area(img, row, col, radius, mask)
                crack_width = search_width_in_table(total_rxw_item_list, radius, crack_area_pixel_num)
                width_list.append(crack_width)

        total_width_list.append(width_list)

    return total_width_list



