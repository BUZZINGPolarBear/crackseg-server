from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.

from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import FileUpload
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import cv2
import os
import json

@csrf_exempt
def fileUpload(request):
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
        resized_img = cv2.resize(resized_img, (448, 448))
        cv2.imwrite('media/resized' +'/resized_'+ str(img).replace(' ', '_'), resized_img)
        cv2.imwrite('templates/static/images/resized/' +'/resized_'+ str(img).replace(' ', '_'), resized_img)

        run_inference_code = "torchrun crack_segmentation/inference_unet.py -model_type resnet34 -img_dir media/resized/ -model_path crack_segmentation/unet_pretrained_false_2/model_best.pt -out_pred_dir templates/static/images/predicted"
        os.system(run_inference_code)
        return HttpResponse(str(img)+" segmantation end")
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
    media_tempalte_resized = "templates/static/images/resized"
    if (os.path.exists(media_imgs)):
        for file in os.scandir((media_imgs)):
            os.remove(file.path)

    if (os.path.exists(media_resized)):
        for file in os.scandir((media_resized)):
            os.remove(file.path)

    if (os.path.exists(media_predicted)):
        for file in os.scandir((media_predicted)):
            os.remove(file.path)

    if (os.path.exists(media_tempalte_resized)):
        for file in os.scandir((media_tempalte_resized)):
            os.remove(file.path)
    return HttpResponse("img remove complated")

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

