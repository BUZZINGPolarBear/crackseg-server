import cv2
import pdb
import os
import argparse as arg
import time
import numpy as np
import params as pm
import table

from dis import dis
from tqdm import tqdm
from importlib.resources import Package
from skimage.morphology import medial_axis
from function import closing_func, opening_func, erode_func, sharpening_func, otsu_func, noise_reduction_func, circle_noise_removal_using_packing_density_func, boundary_func, thinning_func, search_start_interval_point_direction_key, display_start_interval_point, search_edge_segment, display_edge_segment, crack_length_func, adaptive_crack_width_func, profiling_crack_width_func, normal_crack_width_func, profiling_crack_width_func_new

PATH = '/Users/joonhwi/Desktop/KAU/4-2/capstone/aiclops_midterm/'+'aiclops_v5'
IMG_PATH = PATH+'/data/'
SAVE_DIR = PATH+'/results/'

'''API 확인 후 조치 예정'''
parser = arg.ArgumentParser()
parser.add_argument('--data_dir', default=IMG_PATH, help="Directory containing the data")
parser.add_argument('--save_dir', default=SAVE_DIR, help="Directory in which to store results")
parser.add_argument('--mode', default='normal', help="write debug for debug mode")
parser.add_argument('--img_name', default='GQ2_05_2.jpg', help="One image that we want")

# 카메라 렌즈 왜곡 보정 파라미터
parser.add_argument('--FL', default=4.8)
parser.add_argument('--WD', default=0.45)
parser.add_argument('--SIAH', default=14.0)
parser.add_argument('--SRPH', default=9248)

# 입력받은 인자값을 args에 저장 (type: namespace)
args = parser.parse_args()

args.FL = float(args.FL)
args.WD = float(args.WD)
args.SIAH = float(args.SIAH)
args.SRPH = float(args.SRPH)
'''API 확인 후 조치 예정'''

file_name = args.img_name #"RP_03_3.jpg"
img_name = file_name[:-4]

distance = (img_name[-2:]) 
if distance == '10':
    distance = 10 * 1000
else :
    distance = int(distance[1]) * 1000

# print("균열과의 거리", distance, 'mm : ', img_name) # type(distance)
lens = pm.Lens(distance)


def show_result(title, total_length_list, total_width_list, save_dir, distance, lens):
    total_max_width_list = []
    total_average_width_list = []

    for width_block in total_width_list:
        #pdb.set_trace()
        # 너비가 0인 경우는 이미지의 외각에서 벌어나는 인덱스 에러 상황뿐이다. 평균을 구하거나 연산 시 제외
        width_block_zero_removed = [width for width in width_block if width != 0]

        if len(width_block_zero_removed) == 0:
            max_width = 0
            average_width = 0
        else:
            max_width = max(width_block_zero_removed)
            average_width = sum(width_block_zero_removed) / len(width_block_zero_removed)

        total_max_width_list.append(max_width)
        total_average_width_list.append(average_width)
    #

    total_length = sum(total_length_list)
    total_max_width = max(total_max_width_list)
    total_average_width = sum(total_average_width_list) / len(total_average_width_list)


    real_total_max_width_list = lens.real_width(total_max_width_list)
    real_total_average_width_list = lens.real_width(total_average_width_list)
    real_total_max_width = np.array(real_total_max_width_list).max()
    real_total_average_width = sum(real_total_average_width_list) / len(real_total_average_width_list)

    real_total_length_list = lens.real_length(total_length_list)
    real_total_length = sum(real_total_length_list)

    result = zip(total_length_list,
                 real_total_length_list,
                 total_max_width_list,
                 real_total_max_width_list,
                 total_average_width_list,
                 real_total_average_width_list)

    with open("{0}{1}_result.txt".format(save_dir, title), 'w') as f:
        for i, item in enumerate(result, 1):
            f.write('[{0}]\n'
                    'length: {1:.5f}\n'
                    'real_length: {2:.5f}\n'
                    'max_width: {3:.5f}\n'
                    'real_max_width: {4:.5f}\n'
                    'average_width: {5:.5f}\n'
                    'real_average_width: {6:.5f}\n'
                    .format(i, item[0], item[1], item[2], item[3], item[4], item[5]))
        f.write('\n'
                'total_length: {0:.5f}\n'
                'real_total_length: {1:.5f}\n'
                'total_max_width: {2:.5f}\n'
                'real_total_max_width: {3:.5f}\n'
                'total_average_width: {4:.5f}\n'
                'real_total_average_width: {5:.5f}\n'
                '\n'
                .format(total_length, real_total_length, total_max_width, real_total_max_width, total_average_width, real_total_average_width))

    with open("{0}{1}_result_summary.csv".format(save_dir, title), 'w') as f:
        f.write('total_length: {0:.5f}\n'
                'real_total_length: {1:.5f}\n'
                'total_max_width: {2:.5f}\n'
                'real_total_max_width: {3:.5f}\n'
                'total_average_width: {4:.5f}\n'
                'real_total_average_width: {5:.5f}\n'
                '\n'
                .format(total_length, real_total_length, total_max_width, real_total_max_width, total_average_width, real_total_average_width))

    with open("{0}{1}{2}_result_summary.txt".format(save_dir, distance, title), 'w') as f:
        f.write('total_max_width: {0:.5f}\n'
                'real_total_max_width: {1:.5f}\n'
                '\n'
                .format(total_max_width, real_total_max_width))
        print(title,":", real_total_max_width, "\n")
    #
    return 0

###################################################################################################
img_path = '{0}{1}'.format(args.data_dir, file_name)
each_save_dir = '{0}{1}/'.format(args.save_dir, img_name)

if not os.path.exists(each_save_dir):
    os.makedirs(each_save_dir)
    print("made directory")

img = cv2.imread(img_path)
cv2.imwrite(each_save_dir + '{0}_00_original.jpg'.format(img_name), img)

# img_yuv = cv2.cvtColor( cv2.imread(img_path), cv2.COLOR_BGR2YUV)
# #--② 밝기 채널에 대해서 이퀄라이즈 적용
# img_eq = img_yuv.copy()
# img_eq[:,:,0] = cv2.equalizeHist(img_eq[:,:,0])
# img_eq = cv2.cvtColor(img_eq, cv2.COLOR_YUV2BGR)

# # #--③ 밝기 채널에 대해서 CLAHE 적용
# # img_clahe = img_yuv.copy()
# # clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8)) #CLAHE 생성
# # img_clahe[:,:,0] = clahe.apply(img_clahe[:,:,0])           #CLAHE 적용
# # img_clahe = cv2.cvtColor(img_clahe, cv2.COLOR_YUV2BGR)
# cv2.imwrite(each_save_dir + '{0}_00_1_img_clahe.jpg'.format(img_name), img_eq)

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite(each_save_dir + '{0}_01_0_grayscale.jpg'.format(img_name), img)
        
# img = sharpening_func(img)
# cv2.imwrite(each_save_dir + '{0}_01_sharp.jpg'.format(img_name), img)

#2. closing 연산 적용하기 : 검은 색 노이즈 제거
img = closing_func(img)
cv2.imwrite(each_save_dir + '{0}_02_0_closing.jpg'.format(img_name), img)

#3-1. 가우시안 블러 적용 기존 : (7,7) -> (3,3)
img = cv2.GaussianBlur(img, (7, 7), 0)

#3-2 오츄 알고리즘 적용 : 임계값 T로 이진화
img = otsu_func(img)
cv2.imwrite(each_save_dir + '{0}_03_0_otsu.jpg'.format(img_name), img)

# img = erode_func(img)
# cv2.imwrite(each_save_dir + '{0}_03_1_erode.jpg'.format(img_name), img)

#4. 자잘한 노이즈 제거
img = noise_reduction_func(img, threshold=230)
img[0, :] = img[-1, :] = img[:, 0] = img[:, -1] = 0
cv2.imwrite(each_save_dir + '{0}_04_0_noise.jpg'.format(img_name), img)

#5. 큰 덩어리의 노이즈 제거
img = circle_noise_removal_using_packing_density_func(img)
cv2.imwrite(each_save_dir + '{0}_05_circle_noise_.jpg'.format(img_name), img)

#5. 큰 덩어리의 노이즈 제거
# img = circle_noise_removal_using_packing_density_func(img)
# cv2.imwrite(each_save_dir + '{0}_06_circle_noise2_.jpg'.format(img_name), img)


#6. 세선화 과정
img_thinned = thinning_func(img)

#7-1. 분기점(특징점)을 주변 색의 편차를 보고 찾음
start_interval_point_direction_key_list = search_start_interval_point_direction_key(img_thinned)
# print("+++++++++++++",start_interval_point_direction_key_list[0:5])

#7-2. 특징점을 탐색하여, 선분 세그먼트의 시작점부터 끝점을 찾음
total_segment_list, total_chain_list = search_edge_segment(img_thinned, start_interval_point_direction_key_list)

#7-3. 선분 세그먼트의 시작점부터 끝점까지의 길이를 진행한 방향을 통해 계산
total_length_list = crack_length_func(total_chain_list)
#img = img_thinned

#7-4. 균열 선분 이미지에 분기점 시각화하기
color = pm.Color()
img_thinBGR = cv2.cvtColor(img_thinned, cv2.COLOR_GRAY2BGR)
img_length_interval_point = color.display_crack_color(img_thinBGR, total_segment_list, total_length_list, mode='interval_point')
cv2.imwrite(each_save_dir + '{0}_7_img_length_interval_point.jpg'.format(img_name), img_length_interval_point)

#8. 너비 측정
#normal 너비 측정 알고리즘
total_width_list_n = normal_crack_width_func(img, total_segment_list, radius=7)
print(max(total_width_list_n), "//", max(max(total_width_list_n)), lens.real_max_width(max(max(total_width_list_n))))
show_result("normal", total_length_list, total_width_list_n, each_save_dir, distance, lens)
img_width = color.display_crack_color(img_thinBGR, total_segment_list, total_width_list_n, mode='width')
cv2.imwrite(each_save_dir + '{0}_11_normal.jpg'.format(img_name), img_width)

# adaptive 너비 측정 알고리즘
total_width_list_a = adaptive_crack_width_func(img, total_segment_list)
print(max(total_width_list_a), "//", max(max(total_width_list_a)), lens.real_max_width(max(max(total_width_list_a))))
show_result("adaptive", total_length_list, total_width_list_a, each_save_dir, distance, lens)
img_width = color.display_crack_color(img_thinBGR, total_segment_list, total_width_list_a, mode='width')
cv2.imwrite(each_save_dir + '{0}_11_adaptive.jpg'.format(img_name), img_width)

# profiling 너비 측정 알고리즘 - 1
list_old_w, img_pro = profiling_crack_width_func(img, img_thinned, total_chain_list)
print("profiling old:", max(max(list_old_w)), lens.real_max_width(max(max(list_old_w))))
show_result("profiling", total_length_list, list_old_w, each_save_dir, distance, lens)
img_width = color.display_crack_color(img_thinBGR, total_segment_list, list_old_w, mode='width')
cv2.imwrite(each_save_dir + '{0}_11_old.jpg'.format(img_name), img_width)

# profiling 너비 측정 알고리즘 - 2
list_new_w, img_pro = profiling_crack_width_func_new(img, img_thinned, total_chain_list)
print("profiling new:", max(max(list_new_w)), lens.real_max_width(max(max(list_new_w))))
show_result("profiling", total_length_list, list_new_w, each_save_dir, distance, lens)
img_width = color.display_crack_color(img_thinBGR, total_segment_list, list_new_w, mode='width')
cv2.imwrite(each_save_dir + '{0}_11_new.jpg'.format(img_name), img_width)

# print(len(total_chain_list), len(total_segment_list), len(total_width_list_a), total_width_list_a[0], len(total_width_list_n), len(list_old_w), len(list_new_w))