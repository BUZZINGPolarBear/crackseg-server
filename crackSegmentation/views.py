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
        resized_img = cv2.resize(resized_img, (448, 448))
        cv2.imwrite('media/resized' +'/resized_'+ str(title)+'_'+str(length)+'.jpg', resized_img)
        cv2.imwrite('templates/static/images/resized/' +'/resized_'+ str(title)+'_'+str(length)+'.jpg', resized_img)

        run_inference_code = "torchrun crack_segmentation/inference_unet.py -model_type resnet34 -img_dir media/resized/ -model_path crack_segmentation/model/model_best.pt " \
                             "-out_pred_dir templates/static/images/predicted " \
                             "-out_viz_dir templates/static/images/visualized " \
                             "-out_synthesize_dir crack_width_checker/data"
        os.system(run_inference_code)
        return HttpResponse(str(img)+" segmantation end")
    else:
        fileuploadForm = FileUploadForm
        context = {
            'fileuploadForm': fileuploadForm,
        }
        return render(request, 'fileupload.html', context)

'''
이미지를 3*3으로 잘라서 균열 검출
'''
@csrf_exempt
def detailInference(request):
    if request.method == 'POST':
        title = request.POST['title']
        img = request.FILES["imgfile"]

        fileupload = FileUpload(
            title=title,
            imgfile=img,
        )
        fileupload.save()
        print(str(img))
        resized_img = cv2.imread('media/images/' + str(img).replace(' ', '_'))
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

        cv2.imwrite('media/resized' + '/resized_leftTop_' +str(title)+'.jpg', leftTop)
        cv2.imwrite('templates/static/images/resized/' + '/resized_leftTop_' + str(title)+'.jpg', leftTop)
        cv2.imwrite('media/resized' + '/resized_midTop_' + str(title)+'.jpg', midTop)
        cv2.imwrite('templates/static/images/resized/' + '/resized_midTop_' + str(title)+'.jpg', midTop)
        cv2.imwrite('media/resized' + '/resized_rightTop_' + str(title)+'.jpg', rightTop)
        cv2.imwrite('templates/static/images/resized/' + '/resized_rightTop_' + str(title)+'.jpg', rightTop)

        cv2.imwrite('media/resized' + '/resized_leftMid_' + str(title)+'.jpg', leftMid)
        cv2.imwrite('templates/static/images/resized/' + '/resized_leftMid_' + str(title)+'.jpg', leftMid)
        cv2.imwrite('media/resized' + '/resized_midMid_' + str(title)+'.jpg', midMid)
        cv2.imwrite('templates/static/images/resized/' + '/resized_midMid_' + str(title)+'.jpg', midMid)
        cv2.imwrite('media/resized' + '/resized_rightMid_' + str(title)+'.jpg', rightMid)
        cv2.imwrite('templates/static/images/resized/' + '/resized_rightMid_' + str(title)+'.jpg', rightMid)

        cv2.imwrite('media/resized' + '/resized_leftBot_' + str(title)+'.jpg', leftBot)
        cv2.imwrite('templates/static/images/resized/' + '/resized_leftBot_' + str(title)+'.jpg', leftBot)
        cv2.imwrite('media/resized' + '/resized_midBot_' + str(title)+'.jpg', midBot)
        cv2.imwrite('templates/static/images/resized/' + '/resized_midBot_' + str(title)+'.jpg', midBot)
        cv2.imwrite('media/resized' + '/resized_rightBot_' + str(title)+'.jpg', rightBot)
        cv2.imwrite('templates/static/images/resized/' + '/resized_rightBot_' + str(title)+'.jpg', rightBot)
        # TO DO: 이미지 3*3으로 잘라서 저장하기
        # https://wjh2307.tistory.com/7
        run_inference_code = "torchrun crack_segmentation/inference_unet.py -model_type resnet34 -img_dir media/resized/ -model_path crack_segmentation/model/model_best.pt " \
                             "-out_pred_dir templates/static/images/predicted " \
                             "-out_viz_dir templates/static/images/visualized " \
                             "-out_synthesize_dir templates/static/images/analyzed"
        os.system(run_inference_code)
        return HttpResponse(str(img) + " segmantation end")
    else:
        fileuploadForm = FileUploadForm
        context = {
            'fileuploadForm': fileuploadForm,
        }
        return render(request, 'fileupload.html', context)
def testResponse(request):
    return HttpResponse("Hello world!")

@csrf_exempt
def removeImgs(request):
    media_imgs = "media/images/"
    media_resized = "media/resized/"
    media_predicted = "templates/static/images/predicted"
    media_template_resized = "templates/static/images/resized"
    media_template_analyzed = "templates/static/images/analyzed"
    media_template_visualized = "templates/static/images/visualized"
    otsu_data = "crack_width_checker/data"
    otsu_result = "crack_width_checker/results/"

    if (os.path.exists(media_imgs)):
        for file in os.scandir((media_imgs)):
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

    if (os.path.exists(otsu_data)):
        for file in os.scandir((otsu_data)):
            os.remove(file.path)

    if (os.path.exists(otsu_result)):
        shutil.rmtree(otsu_result)
        os.makedirs(otsu_result)

    return HttpResponse("img remove completed")

'''
 비전 추론 알고리즘(오츄) 돌리기
'''
def visionInference(request):
    os.system("python crack_width_checker/main.py")
    return HttpResponse("crack inference algorithm completed")

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

        textFile = open(r'crack_width_checker/results/resized_'+pic_name+'/'+str(length)+'000adaptive_result_summary.txt', "r")
        first_line = textFile.readline().split(' ')[1]
        second_line = textFile.readline().split(' ')[1]
        first_line = re.sub(r'[\n]', '', first_line)
        second_line = re.sub(r'[\n]', '', second_line)
        first_line = float(first_line)
        second_line = float(second_line)

        csvFile = open(r'crack_width_checker/results/resized_'+pic_name+'/adaptive_result_summary.csv', "r")
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
        shutil.copyfile('crack_width_checker/results/resized_'+pic_name+'/resized_'+pic_name+'_8_mask_width_visualization.jpg',
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

