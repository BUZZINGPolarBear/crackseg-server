from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.

from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import FileUpload
from django.views.decorators.csrf import csrf_exempt

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
        return HttpResponse("file-Uploaded")
    else:
        fileuploadForm = FileUploadForm
        context = {
            'fileuploadForm': fileuploadForm,
        }
        return render(request, 'fileupload.html', context)


def testResponse(request):
    return HttpResponse("Hello world!")

