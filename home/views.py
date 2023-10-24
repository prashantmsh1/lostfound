from django.shortcuts import render
import os
# Create your views here.
def home(request):
    image_files = []
    count = 0
    for image_file in os.listdir('static/banner'):
        image_files.append('media/banner/' + image_file )
        count += 1
    context = {
        'image_files': image_files,
        'count': range(0,count),
    }
    print(count)
    return render(request, 'index.html', context)
def parent_sign(request):
    return render(request,'parent_sign.html')
def resque_sign(request):
    return render(request,'resque_sign.html')