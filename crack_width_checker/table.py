import numpy as np
import cv2

from math import ceil
from function import circular_mask, masking_circular_area, write_csv, MIN_CIRCULAR_MASK_RADIUS_RANGE, MAX_CIRCULAR_MASK_RADIUS_RANGE


TEMPLATE_IMAGE_SIZE = 1000                              # 왜 이미지 사이즈를 1000으로 정했지?
TEMPLATE_IMAGE_MID_POINT = int(TEMPLATE_IMAGE_SIZE / 2) # 중점을 500으로 정함

TEMPLATE_IMAGE_CRACK_HALF_LENGTH = 80                   #균열의 반 길이가 뭐하는 상수인가?
MAX_TEMPLATE_IMAGE_CRACK_WIDTH_RANGE = 16               #균열의 너비의 한도는 왜 16인가?

#원으로 마스크하는 반지름의 최대 최소는 7~15
# MIN_CIRCULAR_MASK_RADIUS_RANGE = 7
# MAX_CIRCULAR_MASK_RADIUS_RANGE = 15


def make_template_image():
    # 1000*1000 매트릭스에 0만 채워 넣음 : 검은 이미지
    template_image_background = np.zeros([TEMPLATE_IMAGE_SIZE, TEMPLATE_IMAGE_SIZE]).astype(np.uint8)
    
    #cv2.imshow("hi", template_image_background)
    #cv2.waitKey()
    template_img_list = []
    
    #1부터 15까지 반복 : 크랙의 너비를 1부터 15 중간에 만드는 것
    for width in range(1, MAX_TEMPLATE_IMAGE_CRACK_WIDTH_RANGE):
        template_image = template_image_background.copy()
        template_image[TEMPLATE_IMAGE_MID_POINT - int(width/2): TEMPLATE_IMAGE_MID_POINT + ceil(width/2), TEMPLATE_IMAGE_MID_POINT - TEMPLATE_IMAGE_CRACK_HALF_LENGTH: TEMPLATE_IMAGE_MID_POINT + TEMPLATE_IMAGE_CRACK_HALF_LENGTH] = 255
        #print(TEMPLATE_IMAGE_MID_POINT+ceil(width/2) - (TEMPLATE_IMAGE_MID_POINT-int(width/2)))
        #cv2.imshow('hi', template_image)
        #cv2.waitKey()
        
        #리스트에 1부터 15까지 너비의 크랙 이미지 넣기
        template_img_list.append(template_image)

    return template_img_list


def make_table_rxw_item(template_img_list):
    total_area_list = []
    
    #7부터 15까지
    for radius in range(MIN_CIRCULAR_MASK_RADIUS_RANGE, MAX_CIRCULAR_MASK_RADIUS_RANGE):
        area_list = []
        #중심픽셀을 제외한 반지름이 7부터 15인 꽉찬 흰 원 만드는 함수
        mask, mask_area_pixel_num = circular_mask(radius)
        for template_img in template_img_list:
            #print(radius)
            
            #crack_area_pixel_num를 계산해서 반환
            crack_area_pixel_num = int(
                masking_circular_area(template_img, TEMPLATE_IMAGE_MID_POINT, TEMPLATE_IMAGE_MID_POINT, radius, mask)
            )
            area_list.append(crack_area_pixel_num)
        total_area_list.append(area_list)

    return total_area_list

def make_table():
    template_img_list = make_template_image()
    # print(template_img_list)

    rxw_item = make_table_rxw_item(template_img_list)
    write_csv(rxw_item)


make_table()
