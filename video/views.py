from django.shortcuts import render
# from core.forms import MyFormRegister
from django.shortcuts import render, redirect
from .forms import CustomRegistrationForm

def register(request):
    form = CustomRegistrationForm()
    return render(request, 'django_registration/registration_form.html', context={"form": form})


def video_page(request):
    return render(request, 'video/video_page.html')


def test_video_page(request):
    return render(request, 'video/test_page_video.html')


# def register(requset):
#
#     form = MyFormRegister()
#     return render(requset, 'django_regist/regist.html', context={"form": form})
