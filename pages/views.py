from django.shortcuts import render

# Create your views here.
def indexPage(request):
    return render(request, 'index.html')

def loadingPage(request):
    return render(request, 'index-second.html')

def resultPage(request):
    return render(request, 'index-third.html')