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
from function import *

# 디렉토리를 로컬 폴더 상황에 맞게 변경 요망
PATH = os.getcwd()+'/crack_width_checker'
IMG_PATH = PATH + '/data/org_img/'
MASK_PATH = PATH + '/data/deep_mask/'
SAVE_DIR = PATH + '/results/'

'''API 확인 후 조치 예정'''
parser = arg.ArgumentParser()
parser.add_argument('--img_dir', default=IMG_PATH, help="Directory containing the data")
parser.add_argument('--mask_dir', default=MASK_PATH, help="Directory containing the data")
parser.add_argument('--save_dir', default=SAVE_DIR, help="Directory in which to store results")
parser.add_argument('--mode', default='normal', help="write debug for debug mode")
parser.add_argument('--img_name', default='GQ2_05_2.jpg', help="One image that we want")
parser.add_argument('--width_func', default='adaptive', help="which function to use to calculate crack width")

# 카메라 렌즈 왜곡 보정 파라미터
# parser.add_argument('--FL', default=4.8)
# parser.add_argument('--WD', default=0.45)
# parser.add_argument('--SIAH', default=14.0)
# parser.add_argument('--SRPH', default=9248)

#sony 파라미터
parser.add_argument('--FL', default=12.0)
parser.add_argument('--WD', default=1.0)
parser.add_argument('--SIAH', default=6.287)
parser.add_argument('--SRPH', default=4050)

# 입력받은 인자값을 args에 저장 (type: namespace)
args = parser.parse_args()

args.FL = float(args.FL)
args.WD = float(args.WD)
args.SIAH = float(args.SIAH)
args.SRPH = float(args.SRPH)
'''API 확인 후 조치 예정'''


def show_result(title, total_length_list, total_width_list, save_dir, distance, lens):
    #     for crack_length in total_length_list: #print(crack_length)

    total_max_width_list = []
    total_average_width_list = []
    if len(total_width_list) == 0 : total_width_list.append([0])
    for width_block in total_width_list:
        # pdb.set_trace()
        # 너비가 0인 경우는 이미지의 외각에서 벌어나는 인덱스 에러 상황뿐이다. 평균을 구하거나 연산 시 제외
        width_block_zero_removed = [width for width in width_block if width != 0]

        if len(width_block_zero_removed) == 0:
            max_width = 0
            average_width = 0
        else:
            max_width = try_max(width_block_zero_removed)
            average_width = sum(width_block_zero_removed) / len(width_block_zero_removed)

        total_max_width_list.append(max_width)
        total_average_width_list.append(average_width)
    #
    total_length = sum(total_length_list)
    total_max_width = try_max(total_max_width_list)
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
                .format(total_length, real_total_length, total_max_width, real_total_max_width, total_average_width,
                        real_total_average_width))

    with open("{0}{1}_result_summary.csv".format(save_dir, title), 'w') as f:
        f.write('{0:.5f}\n'
                '{1:.5f}\n'
                '{2:.5f}\n'
                '{3:.5f}\n'
                '{4:.5f}\n'
                '{5:.5f}\n'
                '\n'
                .format(total_length, real_total_length, total_max_width, real_total_max_width, total_average_width,
                        real_total_average_width))

    with open("{0}{1}{2}_result_summary.txt".format(save_dir, distance, title), 'w') as f:
        f.write('total_max_width: {0:.5f}\n'
                'real_total_max_width: {1:.5f}\n'
                '\n'
                .format(total_max_width, real_total_max_width))
        print(title, ":", real_total_max_width, "\n")
    #
    return 0


############################################################################
def main4():
    table.make_table()
    img_index = 0
    for img_file in os.listdir(args.img_dir):  # type: ignore
        if os.path.isdir(args.img_dir + img_file):
            continue
        if os.path.splitext(img_file)[-1] != '.jpg' and os.path.splitext(img_file)[-1] != '.png':
            continue
        if os.path.isdir(args.mask_dir + img_file):
            continue
        if os.path.splitext(img_file)[-1] != '.jpg' and os.path.splitext(img_file)[-1] != '.png':
            continue
        mask_file = os.listdir(args.mask_dir)[img_index]  # type: ignore
        img_index += 1
        print(mask_file)
        start_time = 0.0
        if args.mode == 'debug':
            start_time = time.time()

        img_name = os.path.splitext(img_file)[0]

        distance = (img_name[-2:])
        #       0.25, 0.4, 0.65, 1.2mm
        if distance == '10':
            distance = 10 * 1000
        else:
            distance = int(distance[1]) * 1000
        # print("균열과의 거리", distance, 'mm : ', img_name) # type(distance)

        lens = pm.Lens(distance)

        each_save_dir = '{0}{1}/'.format(args.save_dir, img_name)
        if not os.path.exists(each_save_dir):
            os.makedirs(each_save_dir)  # type: ignore
        img_path = '{0}{1}'.format(args.img_dir, img_file)
        mask_path = '{0}{1}'.format(args.mask_dir, img_file)
        #       print(img_path) # 확인용 디렉토리 출력

        #       1.  전처리할 이미지 불러오기
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # img = cv2.imread(IMG_PATH, cv2.IMREAD_GRAYSCALE)
        print(img_name)
        cv2.imwrite(each_save_dir + '{0}_01_0_grayscale.jpg'.format(img_name), img)

        #       1-1. 딥러닝 마스크 불러오기 - 흑백 영상
        mask = cv2.imread(mask_path, 0)  # mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        resized_mask = cv2.resize(mask, (int(len(img[0])), int(len(img))))
        cv2.imwrite(each_save_dir + '{0}_01_1_mask.jpg'.format(img_name), resized_mask)

        # re_otsu_mask = impacting_func(resized_mask, low=80)
        # cv2.imwrite(each_save_dir + '{0}_01_2_impact_mask.jpg'.format(img_name), re_otsu_mask)
        msk_th, re_otsu_mask = otsu_func(resized_mask)  # threshold_otsu_func(resized_mask, 130)
        cv2.imwrite(each_save_dir + '{0}_01_2_otsu_mask.jpg'.format(img_name), re_otsu_mask)
        th_, re_img = otsu_func(img)  # threshold_otsu_func(resized_mask, 130)

        '''
        mask_thinned = thinning_func(re_otsu_mask)
        mask_thinned = cv2.GaussianBlur(mask_thinned, (9, 9), 0)
        cv2.imwrite(each_save_dir + '{0}_01_3_thin_mask.jpg'.format(img_name), mask_thinned)
        mask_thinned = impacting_func(mask_thinned, low=1)
        # mask_thinned = opening_func(mask_thinned)
        cv2.imwrite(each_save_dir + '{0}_01_4_wide_thin_mask.jpg'.format(img_name), mask_thinned)

        th, otsu_mask = otsu_func(resized_mask)#threshold_otsu_func(resized_mask, 130)
        cv2.imwrite(each_save_dir + '{0}_01_5_otsu_mask.jpg'.format(img_name), resized_mask)
        # otsu_mask = combine_mask(otsu_mask, mask_thinned)
        # cv2.imwrite(each_save_dir + '{0}_01_6_combindes_otsu_mask.jpg'.format(img_name), otsu_mask)

        # for i in range(100, 165, 5):
        #     otsu_mask = adaptive_mean_otsu_func(resized_mask, i)
        #     cv2.imwrite(each_save_dir + '{0}_01_1_{1:.5f}_otsu_mask.jpg'.format(img_name, i), otsu_mask)
        '''

        img = closing_func(img)
        cv2.imwrite(each_save_dir + '{0}_02_0_closing.jpg'.format(img_name), img)

        if th_ - msk_th < 0:
            m = 0
        elif th_ - msk_th < 10:
            m = 7
        elif th_ - msk_th < 20:
            m = 15
        elif th_ - msk_th < 30:
            m = 20
        else:
            m = 5

        if msk_th < 31:
            th = 40
        elif msk_th < 65:
            th = 50
        elif msk_th < 60:
            th = 55
        elif msk_th < 75:
            th = 70
        elif msk_th < 85:
            th = 75
        else:
            th = 80

        print(msk_th, th, m, th - m)

        img = impacting_func(img, low=th - m - 10)  # th-10, 70 #50>65/81>60 , 100>120/85>65
        cv2.imwrite(each_save_dir + '{0}_02_1_closing_impact.jpg'.format(img_name), img)

        #        3-0. 흰색 노이즈 제거
        # img = opening_func(img)
        # cv2.imwrite(SAVE_DIR + '02_opening.png', img)

        # 3-1. 가우시안 블러 적용 기존 : (7,7) -> (3,3)
        if th <= 50:
            img = cv2.GaussianBlur(img, (1, 1), 0)
        elif th <= 75:
            img = cv2.GaussianBlur(img, (3, 3), 0)
        elif th <= 80:
            img = cv2.GaussianBlur(img, (5, 5), 0)
        else:
            img = cv2.GaussianBlur(img, (7, 7), 0)
        cv2.imwrite(each_save_dir + '{0}_03_0_blur.jpg'.format(img_name), img)

        # 3-2 오츄 알고리즘 적용 : 임계값 T로 이진화
        # ?: 적응형 오츄를 사용하지 않은 이유가 무엇인가?(야외라서, 빛의 영향이 골고루 반영되기 때문, 처음에 closing을 해서? : 균열 내부가 비기 때문에
        if th < 45:
            th, otsu_img = threshold_otsu_func(img, th=th)  # otsu_func(img)
        else:
            th, otsu_img = threshold_otsu_func(img, th=th - m - 15)  # otsu_func(img)
        cv2.imwrite(each_save_dir + '{0}_03_otsu.jpg'.format(img_name), otsu_img)

        #        4. 자잘한 노이즈 제거
        img = noise_reduction_func(otsu_img, threshold=185)  # 220~230
        img[0, :] = img[-1, :] = img[:, 0] = img[:, -1] = 0
        cv2.imwrite(each_save_dir + '{0}_04_noise_reduction.jpg'.format(img_name), img)

        #        5. 큰 덩어리의 노이즈 제거
        img = circle_noise_removal_using_packing_density_func(img)
        cv2.imwrite(each_save_dir + '{0}_05_0_circle_noise_removal.jpg'.format(img_name), img)

        # if msk_th >= 80:
        #     img = cv2.GaussianBlur(img, (3, 3), 1)
        #     cv2.imwrite(each_save_dir + '{0}_05_1_noise_removal_blur.jpg'.format(img_name), img)

        #        5-1. 노이즈 제거 영상과 딥러닝 마스크 and 연산
        img_and_mask = combine_mask(img, re_otsu_mask)
        cv2.imwrite(each_save_dir + '{0}_05_2_and_mask.jpg'.format(img_name), img_and_mask)

        # if msk_th >= 80:
        #
        #     j = impacting_func(img_and_mask, low=th+10)
        #     th, img_and_mask= threshold_otsu_func(img_and_mask,th=min(msk_th+10, 230)) #otsu_func(j)
        img_and_mask[0, :] = img_and_mask[-1, :] = img_and_mask[:, 0] = img_and_mask[:, -1] = 0
        cv2.imwrite(each_save_dir + '{0}_05_3_and_impact.jpg'.format(img_name), img_and_mask)

        if msk_th < 80:
            img_and_mask_ = cv2.GaussianBlur(img_and_mask, (7, 7), 1)
            ret2, img_and_mask_= threshold_otsu_func(img_and_mask_, th=220)  # otsu_func(img)
        else:
            img_and_mask_ = cv2.GaussianBlur(img_and_mask, (7, 7), 1)
            ret2, img_and_mask_ = threshold_otsu_func(img_and_mask_, th=240)  # otsu_func(img)

        if find_max(img_and_mask_) == 0:
            img_and_mask = img_and_mask_
            print("empty image - go back")
        cv2.imwrite(each_save_dir + '{0}_05_4_and_mask_blur.jpg'.format(img_name), img_and_mask)


        #        6. 세선화 과정
        img_thinned = thinning_func(img_and_mask)
        cv2.imwrite(each_save_dir + '{0}_06_thinning.jpg'.format(img_name), img_thinned)

        #        7. 세선화된 영상에서 각 edge(crack의 뼈대)의 시작점 및 분기점을 검출

        #        7-1. 분기점(특징점)을 주변 색의 편차를 보고 찾음 : (특징점좌표, 이웃 하얀 픽셀 좌표)원소
        start_interval_point_direction_key_list = search_start_interval_point_direction_key(img_thinned)

        #        7-2. 특징점을 탐색하여, 선분 세그먼트의 시작점부터 끝점을 찾음
        total_segment_list, total_chain_list = search_edge_segment(img_thinned, start_interval_point_direction_key_list)

        #        7-3. 선분 세그먼트의 시작점부터 끝점까지의 길이를 진행한 방향을 통해 계산
        total_length_list = crack_length_func(total_chain_list)

        # img_crack_length = display_crack_length(img_thinned, total_segment_list, total_length_list)
        # cv2.imwrite(each_save_dir+'{0}_case3_10_crack_length_visualization.png'.format(img_name), img_crack_length)

        #        7-4. 균열 선분 이미지에 분기점 시각화하기
        color = pm.Color()
        img_thinBGR = cv2.cvtColor(img_thinned, cv2.COLOR_GRAY2BGR)
        img_BGR = cv2.cvtColor(img_and_mask, cv2.COLOR_GRAY2BGR)
        # for i, j, _ in start_interval_point_direction_key_list: cv2.circle(img_thinBGR, (j, i), 10, (0, 255, 0), thickness=3)
        img_length_interval_point = color.display_crack_color(img_thinBGR, total_segment_list, total_length_list,
                                                              mode='interval_point')
        cv2.imwrite(each_save_dir + '{0}_7_0_img_length_interval_point.jpg'.format(img_name), img_length_interval_point)
        img_length_interval_point = color.display_crack_color(img_BGR, total_segment_list, total_length_list,
                                                              mode='interval_point')
        cv2.imwrite(each_save_dir + '{0}_7_1_full_length_interval_point.jpg'.format(img_name),
                    img_length_interval_point)

        #        8. 선분의 너비를 구하기 위한 함수
        #        8-1. 폭을 계산한 리스트 만들기(모든 균열 포인트마다)
        #        default : adaptive
        #        usable width func : normal, adaptive, profiling_1 profiling_2
        if args.width_func == 'adaptive':
            total_width_list = adaptive_crack_width_func(img_and_mask, total_segment_list)
        elif args.width_func == 'normal':
            total_width_list = normal_crack_width_func(img_and_mask, total_segment_list, radius=7)
        elif args.width_func == 'profiling_1':
            total_width_list, img_pro = profiling_crack_width_func(img_and_mask, img_thinned, total_chain_list)
        elif args.width_func == 'profiling_re':
            total_width_list, img_pro = renewal_profiling_crack_width_func(img_and_mask, img_thinned,
                                                                           total_segment_list, total_chain_list)
        else:
            total_width_list, img_pro = profiling_crack_width_func_new(img_and_mask, img_thinned, total_chain_list)

        #        8-2. 균열 선분 이미지에 폭을 색상으로 시각화하기
        img_width = color.display_crack_color(img_thinBGR, total_segment_list, total_width_list, mode='width')
        cv2.imwrite(each_save_dir + '{0}_8_thin_width_visualization.jpg'.format(img_name), img_width)

        #        8-3. 균열 이미지에 폭을 색상으로 시각화하기
        img_full_width = fill_crack_width_func(img_and_mask, img_thinned, total_segment_list, total_chain_list,
                                               total_width_list)
        cv2.imwrite(each_save_dir + '{0}_9_full_width_visualization.jpg'.format(img_name), img_full_width)

        show_result(args.width_func, total_length_list, total_width_list, each_save_dir, distance, lens)

        if args.mode == 'debug':
            end_time = time.time()
            cost_time = end_time - start_time
            print('cost time of {0}: {1}'.format(img_file, cost_time))

        if args.mode == 'debug':
            cv2.imwrite(each_save_dir + '{0}_case4_03_otsu_img.jpg'.format(img_name),
                        otsu_img)
            img_start_interval_point = display_start_interval_point(img_thinned,
                                                                    start_interval_point_direction_key_list)
            # cv2.imwrite(SAVE_DIR+'08_start_interval_point.png', img_start_interval_point)
            img_edge_segment_followed = display_edge_segment(img_thinned, total_segment_list)
            # cv2.imwrite(SAVE_DIR+'09_edge_segment_followed.png', img_edge_segment_followed)

            # 해당 함수를 찾을 수 없음
            cv2.imshow('hi', img_length_interval_point)
            cv2.waitKey()
            cv2.imshow('hi', img_width)
            cv2.waitKey()

    return True


if __name__ == '__main__':
    main4()



