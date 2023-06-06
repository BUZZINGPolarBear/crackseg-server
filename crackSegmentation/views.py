from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
# Create your views here.

from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import FileUpload
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import csv
import cv2
import os
import json
import re
import shutil

'''
이미지를 다운받아서 한번에 균열 검출
'''
@csrf_exempt
def fileUpload(request):
    if request.method == 'POST':
        title = request.POST['title']
        img = request.FILES["imgfile"]
        length = request.POST['length']

        fileupload = FileUpload(
            title=title,
            imgfile=img,
        )
        fileupload.save()

        resized_img = cv2.imread('media/images/' + str(img).replace(' ', '_'))
        width = resized_img.shape[1]
        height = resized_img.shape[0]
        resized_img = cv2.resize(resized_img, (448, 448))
        cv2.imwrite('media/resized' +'/resized_'+ str(title)+'_'+str(length)+'.jpg', resized_img)
        cv2.imwrite('crack_width_checker/data/org_img' + '/resized_' + str(title) + '_' + str(length) + '.jpg', resized_img)
        cv2.imwrite('templates/static/images/resized/' +'/resized_'+ str(title)+'_'+str(length)+'.jpg', resized_img)

        run_inference_code = "torchrun crack_segmentation/inference_unet.py -model_type resnet34 -img_dir media/resized/ -model_path crack_segmentation/model/model_best.pt " \
                             "-out_pred_dir templates/static/images/predicted " \
                             "-out_viz_dir templates/static/images/visualized " \
                             "-out_synthesize_dir crack_width_checker/data/deep_mask"
        os.system(run_inference_code)
        result = {
            "status": 'ok',
            "code" : 200,
            "width" : width,
            "height" : height,
            "message": str(img) + "segmentation end"
        }
        return JsonResponse(result)
    else:
        fileuploadForm = FileUploadForm
        context = {
            'fileuploadForm': fileuploadForm,
        }
        return render(request, 'fileupload.html', context)

'''
이미지를 448*448*n으로 크롭할 수 있도록 패딩 추가 후 잘라서 균열 검출
'''
@csrf_exempt
def detailInference(request):
    if request.method == 'POST':
        title = request.POST['title']
        img = request.FILES["imgfile"]
        length = request.POST['length']

        fileupload = FileUpload(
            title=title,
            imgfile=img,
        )
        fileupload.save()

        userImg = cv2.imread('media/images/' + str(img).replace(' ', '_'))
        cv2.imwrite('templates/static/images/origin/' + str(title) + '_' + str(length) + '.jpg', userImg)
        resized_img = cv2.imread('media/images/' + str(img).replace(' ', '_'))

        width = userImg.shape[1]
        height = userImg.shape[0]

        if width > 1344 & height > 1344:
            resized_img = resized_img[(height-1344)//2:((height-1344)//2)+1344, (width-1344)//2:((width-1344)//2)+1344]
        else: resized_img = cv2.resize(resized_img, (1344, 1344))


        objectWidth = 0
        objectHeight = 0
        while width > objectWidth:
            objectWidth += 448
        while height > objectHeight:
            objectHeight += 448

        widthDiffer = (objectWidth - width) // 2
        heightDiffer = (objectHeight - height)//2
        average = userImg.mean(axis=0).mean(axis=0)
        addZeroPadding = cv2.copyMakeBorder(userImg,
                                            heightDiffer,
                                            heightDiffer,
                                            widthDiffer,
                                            widthDiffer,
                                            cv2.BORDER_CONSTANT,
                                            value=average
                                            )

        cv2.imwrite('media/paddingAdded/' + str(title) + '_' + str(length) + '.jpg', addZeroPadding)

        row_cnt = objectWidth//448
        col_cnt = objectHeight//448

        resized_img = cv2.resize(resized_img, (1344, 1344))

        leftTop = resized_img[0:448, 0:448]
        midTop = resized_img[0: 448, 448: 896]
        rightTop = resized_img[0: 448, 896: 1344]

        leftMid = resized_img[448:896, 0: 448]
        midMid = resized_img[448:896, 448: 896]
        rightMid = resized_img[448:896, 896:1344]

        leftBot = resized_img[896:1344, 0:448]
        midBot = resized_img[896:1344, 448:896]
        rightBot = resized_img[896:1344, 896:1344]

        cv2.imwrite('media/resized' + '/resized_leftTop_' + str(title) + '_' + str(length) + '.jpg', leftTop)
        cv2.imwrite('crack_width_checker/data/org_img' + '/resized_leftTop_' + str(title) + '_' + str(length) + '.jpg', leftTop)
        cv2.imwrite('templates/static/images/resized/' + '/resized_leftTop_' + str(title) + '_' + str(length) + '.jpg',
                    leftTop)
        cv2.imwrite('media/resized' + '/resized_midTop_' + str(title) + '_' + str(length) + '.jpg', midTop)
        cv2.imwrite('crack_width_checker/data/org_img' + '/resized_midTop_' + str(title) + '_' + str(length) + '.jpg', midTop)
        cv2.imwrite('templates/static/images/resized/' + '/resized_midTop_' + str(title) + '_' + str(length) + '.jpg',
                    midTop)
        cv2.imwrite('media/resized' + '/resized_rightTop_' + str(title) + '_' + str(length) + '.jpg', rightTop)
        cv2.imwrite('crack_width_checker/data/org_img' + '/resized_rightTop_' + str(title) + '_' + str(length) + '.jpg', rightTop)
        cv2.imwrite('templates/static/images/resized/' + '/resized_rightTop_' + str(title) + '_' + str(length) + '.jpg',
                    rightTop)

        cv2.imwrite('media/resized' + '/resized_leftMid_' + str(title) + '_' + str(length) + '.jpg', leftMid)
        cv2.imwrite('crack_width_checker/data/org_img' + '/resized_leftMid_' + str(title) + '_' + str(length) + '.jpg', leftMid)
        cv2.imwrite('templates/static/images/resized/' + '/resized_leftMid_' + str(title) + '_' + str(length) + '.jpg',
                    leftMid)
        cv2.imwrite('media/resized' + '/resized_midMid_' + str(title) + '_' + str(length) + '.jpg', midMid)
        cv2.imwrite('crack_width_checker/data/org_img' + '/resized_midMid_' + str(title) + '_' + str(length) + '.jpg', midMid)
        cv2.imwrite('templates/static/images/resized/' + '/resized_midMid_' + str(title) + '_' + str(length) + '.jpg',
                    midMid)
        cv2.imwrite('media/resized' + '/resized_rightMid_' + str(title) + '_' + str(length) + '.jpg', rightMid)
        cv2.imwrite('crack_width_checker/data/org_img' + '/resized_rightMid_' + str(title) + '_' + str(length) + '.jpg', rightMid)
        cv2.imwrite('templates/static/images/resized/' + '/resized_rightMid_' + str(title) + '_' + str(length) + '.jpg',
                    rightMid)

        cv2.imwrite('media/resized' + '/resized_leftBot_' + str(title) + '_' + str(length) + '.jpg', leftBot)
        cv2.imwrite('crack_width_checker/data/org_img' + '/resized_leftBot_' + str(title) + '_' + str(length) + '.jpg', leftBot)
        cv2.imwrite('templates/static/images/resized/' + '/resized_leftBot_' + str(title) + '_' + str(length) + '.jpg',
                    leftBot)
        cv2.imwrite('media/resized' + '/resized_midBot_' + str(title) + '_' + str(length) + '.jpg', midBot)
        cv2.imwrite('crack_width_checker/data/org_img' + '/resized_midBot_' + str(title) + '_' + str(length) + '.jpg', midBot)
        cv2.imwrite('templates/static/images/resized/' + '/resized_midBot_' + str(title) + '_' + str(length) + '.jpg',
                    midBot)
        cv2.imwrite('media/resized' + '/resized_rightBot_' + str(title) + '_' + str(length) + '.jpg', rightBot)
        cv2.imwrite('crack_width_checker/data/org_img' + '/resized_rightBot_' + str(title) + '_' + str(length) + '.jpg', rightBot)
        cv2.imwrite('templates/static/images/resized/' + '/resized_rightBot_' + str(title) + '_' + str(length) + '.jpg',
                    rightBot)


        row_col_info = {
            "status": 'ok',
            "code": 200,
            'row_line': row_cnt,
            'col_line': col_cnt,
        }
        return JsonResponse(row_col_info)
    else:
        fileuploadForm = FileUploadForm
        context = {
            'fileuploadForm': fileuploadForm,
        }
        return render(request, 'fileupload.html', context)

def runDetailInference(request):
    run_inference_code = "torchrun crack_segmentation/inference_unet.py " \
                         "-model_type resnet34 " \
                         "-img_dir media/resized/ " \
                         "-model_path crack_segmentation/model/model_best.pt " \
                         "-out_pred_dir templates/static/images/predicted " \
                         "-out_viz_dir templates/static/images/visualized " \
                         "-out_synthesize_dir crack_width_checker/data/deep_mask"
    print(run_inference_code)
    os.system(run_inference_code)
    result = {
        "status": 'ok',
        "code": 200,
        "message": "detailed inference code done"
    }
    return JsonResponse(result)

def get_image_files(directory):
    image_files = []
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            try:
                img = Image.open(file_path)
                img.verify()  # 이미지 유효성 확인
                image_files.append(file)
            except (IOError, SyntaxError):
                # 유효하지 않은 이미지 파일
                pass
    return image_files

def rename_image_file(file_path, new_file_name):
    directory, old_file_name = os.path.split(file_path)
    new_file_path = os.path.join(directory, new_file_name)
    os.rename(file_path, new_file_path)

def runMQDetailInference(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)

            # 필요한 데이터 추출
            op = json_data['header']['op']
            type = json_data['header']['type']
            tid = json_data['header']['tid']
            msgFrom = json_data['header']['msgFrom']
            timestamp = json_data['header']['timestamp']
            origId = json_data['body']['origId']
            analysisId = json_data['body']['analysisId']
            index = json_data['body']['index']
            fileDir = json_data['body']['fileDir']
            distance = json_data['body']['distance']

            result_dict = {}
            result_arr = []

            origin_dir = get_image_files(fileDir)
            for pic_name in origin_dir:
                # print(pic_name)
                distance_meter: int
                try:
                    distance_meter = distance.split('.')[0]
                except:
                    distance_meter = 1
                rename_image_file(fileDir + pic_name,
                                  f"{pic_name.split('.')[0]}_{distance_meter}.{pic_name.split('.')[1]}")

            run_inference_code = "torchrun crack_segmentation/inference_unet.py " \
                                 "-model_type resnet34 " \
                                 f"-img_dir {fileDir} " \
                                 "-model_path crack_segmentation/model/model_best.pt " \
                                 f"-out_pred_dir {fileDir}/{origId}-prediction/ " \
                                 "-out_viz_dir templates/static/images/visualized " \
                                 "-out_synthesize_dir crack_width_checker/data/deep_mask"

            os.system(run_inference_code)

            os.system(
                f"python crack_width_checker/vision.py --width_func profiling_re --img_dir {fileDir}  --mask_dir {fileDir}{origId}-prediction/ --save_dir {fileDir}{origId}-prediction/results")

            image_files = get_image_files(f"{fileDir}{origId}-prediction/")
            # print(image_files)
            inference_index = 0
            for pic_name in image_files:
                orig_pic_name = pic_name
                pic_name = pic_name.split('.')[0]
                distance = pic_name.split('_')[-1]
                if os.path.exists(
                        f'{fileDir}{origId}-prediction/results{pic_name}/{distance}000profiling_re_result_summary.txt'):
                    textFile = open(
                        f'{fileDir}{origId}-prediction/results{pic_name}/{distance}000profiling_re_result_summary.txt',
                        "r")
                    first_line = textFile.readline().split(' ')[1]
                    second_line = textFile.readline().split(' ')[1]
                    first_line = re.sub(r'[\n]', '', first_line)
                    second_line = re.sub(r'[\n]', '', second_line)
                    first_line = float(first_line)
                    second_line = float(second_line)

                    csvFile = open(f'{fileDir}{origId}-prediction/results{pic_name}/profiling_re_result_summary.csv',
                                   "r")
                    # print(f'{fileDir}{origId}-prediction/results{pic_name}/profiling_re_result_summary.csv')
                    csvReader = csv.reader(csvFile)


                    all_crack_length = 0.0
                    average_crack_width = 0.0

                    csv_index = 1
                    for line in csvReader:
                        # print(f"CSV LINE: {line}")
                        if csv_index == 1: all_crack_length = float(line[0])
                        if csv_index == 5: average_crack_width = float(line[0])
                        csv_index += 1

                    crack_info_dict = {
                        "originId": origId,
                        "analysisId": analysisId,
                        "index": inference_index,
                        "fileDir": f"{fileDir}{origId}-prediction/{orig_pic_name}",
                        "crackInfo": {
                            "totalLength": all_crack_length,
                            "aveWidth": average_crack_width,
                            "maxWidth": second_line,
                        }
                    }
                    inference_index += 1
                    result_arr.append(crack_info_dict)
            result_dict = {"header": json_data['header'], "body": result_arr}
            return JsonResponse(result_dict)

        except:
            response_data = {
            'status': 'error',
            'message': '부적절한 형식입니다.'
            }
            return JsonResponse(response_data, status=405)

def testResponse(request):
    return HttpResponse("Hello world!")

@csrf_exempt
def removeImgs(request):
    if request.method == 'POST':
        request_body = json.loads(request.body)
        file_name = request_body["img_name"]
        original_file_name = request_body["original_file_name"]

        media_imgs = "media/images/"+original_file_name
        media_resized = "media/resized/resized_"+file_name.split('.')[0]+".jpg"
        media_predicted = "templates/static/images/predicted/resized_"+file_name.split('.')[0]+".jpg"
        media_predicted2 = "templates/static/images/predicted/1344*1344_converted_resized_" + file_name.split('.')[0] + ".jpg"
        media_template_resized = "templates/static/images/resized/resized_"+file_name.split('.')[0]+".jpg"
        media_template_analyzed = "templates/static/images/analyzed/analyzed_"+file_name.split('.')[0]+".jpg"
        media_template_visualized = "templates/static/images/visualized/resized_"+file_name.split('.')[0]+".jpg"
        otsu_data = "crack_width_checker/data/resized_"+file_name.split('.')[0]+".jpg"
        otsu_result = "crack_width_checker/results/resized_"+file_name.split('.')[0]

        if (os.path.isfile(media_imgs)):
                os.remove(media_imgs)

        if (os.path.isfile(media_resized)):
                os.remove(media_resized)

        if (os.path.isfile(media_predicted)):
                os.remove(media_predicted)

        if (os.path.isfile(media_predicted2)):
            os.remove(media_predicted2)

        if (os.path.isfile(media_template_resized)):
                os.remove(media_template_resized)

        if (os.path.isfile(media_template_analyzed)):
                os.remove(media_template_analyzed)

        if (os.path.isfile(media_template_visualized)):
                os.remove(media_template_visualized)

        if (os.path.isfile(otsu_data)):
                os.remove(otsu_data)

        if (os.path.isfile(otsu_result)):
            os.remove(otsu_result)

        result = {
            "status": 'ok',
            "code": 200,
            "message": "img remove done"
        }
        return JsonResponse(result)
    if request.method == 'GET':
        media_imgs = "media/images/"
        media_paddingAdded = "media/paddingAdded/"
        media_cropped = "media/cropped/"
        media_resized = "media/resized/"
        media_predicted = "templates/static/images/predicted"
        media_template_resized = "templates/static/images/resized"
        media_template_analyzed = "templates/static/images/analyzed"
        media_template_cropped = "templates/static/images/cropped"
        media_template_visualized = "templates/static/images/visualized"
        media_template_origin = "templates/static/images/origin"
        otsu_data_deep_mask = "crack_width_checker/data/deep_mask"
        otsu_data_org_img = "crack_width_checker/data/org_img"
        otsu_result = "crack_width_checker/results/"

        if (os.path.exists(media_imgs)):
            for file in os.scandir((media_imgs)):
                os.remove(file.path)

        if (os.path.exists(media_paddingAdded)):
            for file in os.scandir((media_paddingAdded)):
                os.remove(file.path)

        if (os.path.exists(media_cropped)):
            for file in os.scandir((media_cropped)):
                os.remove(file.path)

        if (os.path.exists(media_resized)):
            for file in os.scandir((media_resized)):
                os.remove(file.path)

        if (os.path.exists(media_predicted)):
            for file in os.scandir((media_predicted)):
                os.remove(file.path)

        if (os.path.exists(media_template_resized)):
            for file in os.scandir((media_template_resized)):
                os.remove(file.path)

        if (os.path.exists(media_template_analyzed)):
            for file in os.scandir((media_template_analyzed)):
                os.remove(file.path)

        if (os.path.exists(media_template_visualized)):
            for file in os.scandir((media_template_visualized)):
                os.remove(file.path)

        if (os.path.exists(media_template_origin)):
            for file in os.scandir((media_template_origin)):
                os.remove(file.path)

        if (os.path.exists(media_template_cropped)):
            for file in os.scandir((media_template_cropped)):
                os.remove(file.path)

        if (os.path.exists(otsu_data_deep_mask)):
            for file in os.scandir((otsu_data_deep_mask)):
                os.remove(file.path)
        if (os.path.exists(otsu_data_org_img)):
            for file in os.scandir((otsu_data_org_img)):
                os.remove(file.path)

        if (os.path.exists(otsu_result)):
            shutil.rmtree(otsu_result)
            os.makedirs(otsu_result)

        result = {
            "status": 'ok',
            "code": 200,
            "message": "img remove done"
        }
        return JsonResponse(result)

'''
    디테일 사진 추론할 떄 안쓸 사진 지우기
'''
@csrf_exempt
def removeUnusefulImgs(request):
    if request.method == 'POST':
        request_body = json.loads(request.body)
        usefulImgs = request_body['selectedPicArray']

        for i in range(0, len(usefulImgs)):
            if(os.path.exists("media/resized/" + usefulImgs[i])):
                os.remove("media/resized/" + usefulImgs[i])
            if (os.path.exists("crack_width_checker/data/org_img/" + usefulImgs[i])):
                os.remove("crack_width_checker/data/org_img/" + usefulImgs[i])

        return HttpResponse("remove completed")
'''
 비전 추론 알고리즘(오츄) 돌리기
'''
def visionInference(request):
    fileDir = request.GET.get("fileDir")
    origId = request.GET.get("origId")
    os.system(f"python crack_width_checker/vision.py --width_func profiling_re --img_dir {fileDir}/{origId}-prediction/ --save_dir {fileDir}/{origId}-prediction/results")
    result = {
        "status": 'ok',
        "code": 200,
        "message": "vision inference code done"
    }
    return JsonResponse(result)

'''
비전추론 결과 가져오기
'''
@csrf_exempt
def visionInferenceInfo(request):
    if request.method == 'POST':
        request_body = json.loads(request.body)
        pic_name = request_body['img_name']
        length = request_body['length']
        pic_name = pic_name.split('.')[0]
        if os.path.exists('crack_width_checker/results/resized_'+pic_name+'/'+str(length)+'000profiling_re_result_summary.txt'):
            textFile = open(r'crack_width_checker/results/resized_'+pic_name+'/'+str(length)+'000profiling_re_result_summary.txt', "r")
            first_line = textFile.readline().split(' ')[1]
            second_line = textFile.readline().split(' ')[1]
            first_line = re.sub(r'[\n]', '', first_line)
            second_line = re.sub(r'[\n]', '', second_line)
            first_line = float(first_line)
            second_line = float(second_line)

            csvFile = open(r'crack_width_checker/results/resized_'+pic_name+'/profiling_re_result_summary.csv', "r")
            csvReader = csv.reader(csvFile)

            index = 0
            all_crack_length = 0.0
            average_crack_width = 0.0
            for line in csvReader:
                if index == 1: all_crack_length = float(line[0])
                if index == 5: average_crack_width = float(line[0])
                index += 1

            crack_info_dict = {
                'real_max_width': second_line,
                'all_crack_length' : all_crack_length,
                'average_crack_width': average_crack_width
            }
            shutil.copyfile('crack_width_checker/results/resized_'+pic_name+'/resized_'+pic_name+'_9_full_width_visualization.jpg',
                            'templates/static/images/analyzed/analyzed_'+pic_name+'.jpg')

            return JsonResponse(crack_info_dict)

@csrf_exempt
def rabbitVisionInferenceInfo(request):
    if request.method == 'POST':
        request_body = json.loads(request.body)
        pic_name = request_body['img_name']
        length = request_body['length']
        pic_name = pic_name.split('.')[0]
        if os.path.exists('crack_width_checker/results/resized_'+pic_name+'/'+str(length)+'000profiling_re_result_summary.txt'):
            textFile = open(r'crack_width_checker/results/resized_'+pic_name+'/'+str(length)+'000profiling_re_result_summary.txt', "r")
            first_line = textFile.readline().split(' ')[1]
            second_line = textFile.readline().split(' ')[1]
            first_line = re.sub(r'[\n]', '', first_line)
            second_line = re.sub(r'[\n]', '', second_line)
            first_line = float(first_line)
            second_line = float(second_line)

            csvFile = open(r'crack_width_checker/results/resized_'+pic_name+'/profiling_re_result_summary.csv', "r")
            csvReader = csv.reader(csvFile)

            index = 0
            all_crack_length = 0.0
            average_crack_width = 0.0
            for line in csvReader:
                if index == 1: all_crack_length = float(line[0])
                if index == 5: average_crack_width = float(line[0])
                index += 1

            crack_info_dict = {
                'real_max_width': second_line,
                'all_crack_length' : all_crack_length,
                'average_crack_width': average_crack_width
            }
            shutil.copyfile('crack_width_checker/results/resized_'+pic_name+'/resized_'+pic_name+'_9_full_width_visualization.jpg',
                            'templates/static/images/analyzed/analyzed_'+pic_name+'.jpg')

            return JsonResponse(crack_info_dict)


def rescale(image, width):
    img = Image.open(image)

    src_width, src_height = img.size
    src_ratio = float(src_height) / float(src_width)
    dst_height = round(src_ratio * width)

    img = img.resize((width, dst_height), Image.LANCZOS)
    img.save(image.name, 'JPEG')
    image.file = img

    # 이게 없으면 attribute error 발생
    image.file.name = image.name

    return image

