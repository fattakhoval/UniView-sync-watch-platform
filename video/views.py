from django.shortcuts import render

def video_page(request):
    return render(request, 'video/video_page.html')


def test_video_page(request):
    return render(request, 'video/test_page_video.html')
