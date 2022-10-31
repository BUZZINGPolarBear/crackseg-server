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
        cv2.imwrite('media/resized/' +'resized_'+ str(img), resized_img)
        # os.system("명령어")
        return HttpResponse(str(img)+" file-Uploaded")
    else:
        fileuploadForm = FileUploadForm
        context = {
            'fileuploadForm': fileuploadForm,
        }
        return render(request, 'fileupload.html', context)


def testResponse(request):
    return HttpResponse("Hello world!")


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

