from django.shortcuts import render
from core.forms import MyFormRegister


def video_page(request):
    return render(request, 'video/video_page.html')


def test_video_page(request):
    return render(request, 'video/test_page_video.html')


def register(requset):

    form = MyFormRegister()
    return render(requset, 'django_regist/regist.html', context={"form": form})
