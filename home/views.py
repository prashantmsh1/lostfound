
from django.forms import ImageField
from django.shortcuts import render
import os
from django.shortcuts import redirect
from .models import *
import pickle
import face_recognition 
from PIL import Image
import os


# Create your views here.
from PIL import Image
from django.core.files.storage import default_storage

def childdata(request):
    
    data=request.POST
    child_name=data.get('child_name')
    child_age=data.get('child_age')
    location=data.get('location')
    child_image=request.FILES.get('child_image')
    
    Child.objects.create(child_name=child_name,
                         child_age=child_age,
                         location=location,
                         child_image=child_image)
    
    
    with open("known_data.pkl", "rb") as file:
         known_data = pickle.load(file)

    known_faces = known_data["known_faces"]
    known_images = known_data["known_images"]
    
    unknown_image = face_recognition.load_image_file("test.jpg")
    unknown_face_encodings = face_recognition.face_encodings(unknown_image)
    if len(unknown_face_encodings) > 0:
        unknown_face_encoding = unknown_face_encodings[0]
    
    # Compare the unknown face to the known faces
        results = face_recognition.compare_faces(known_faces, unknown_face_encoding)

        if True in results:
        # Match found
            match_index = results.index(True)
            matched_image = known_images[match_index]
            matched_image.show()
            destination_path = 'static/matched/matched_image.jpg'
            matched_image.save(destination_path)
            print(f"Match found: {matched_image}")
            
        else:
        # No match found
            print("No match found")
    else:
    # No face found in the unknown image
        print("No face found in the unknown image")
    return (destination_path)

def home(request):
    image_files = []
    count = 0
    for image_file in os.listdir('static/banner'):
        image_files.append(f'media/banner/{image_file}')
        count += 1
    context = {
        'image_files': image_files,
        'count': range(count),
    }
    print(count)
    return render(request, 'index.html', context)
def parent_sign(request):
    return render(request,'parent_sign.html')
def parent_login(request):
    return render(request,'parent_login.html')
def resque_sign(request):
    return render(request,'resque_sign.html')
def resque_login(request):
    return render(request,'resque_login.html')
def resque_dash(request):
    match=""
    if request.method == "POST":
        match=childdata(request)
        path = match.split("/")
        path[0] = "media"
        match="/"+"/".join(path)
        
    Child.objects.all().delete()
    import os

# Get the full path to the static/child_image folder
    static_child_image_folder_path = os.path.join('static/child_image')

# Get a list of all the files in the static/child_image folder
    static_child_image_files = os.listdir(static_child_image_folder_path)

# Iterate over the files and delete them
    for file in static_child_image_files:
        os.remove(os.path.join(static_child_image_folder_path, file))


        
        
    return render(request,'resque_dash.html',{'match':match})

def parent_dash(request):
    return render(request,'parent_dash.html')