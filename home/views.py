
from django.forms import ImageField
from django.http import HttpResponse
from django.shortcuts import render
import os
from django.shortcuts import redirect
from .models import *
import pickle
import face_recognition 
from PIL import Image
import os
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login

# Create your views here.
from PIL import Image
from django.core.files.storage import default_storage

def childdata(request):
    
    data=request.POST
    child_name=data.get('child_name')
    child_age=data.get('child_age')
    location=data.get('location')
    child_image=request.FILES.get('child_image')
    child_height=data.get('child_height')
    birth_mark=data.get('birth_mark')

    Child.objects.create(child_name=child_name,
                         child_age=child_age,
                         location=location,
                         child_image=child_image,
                         child_height=child_height,
                         birth_mark=birth_mark)


    with open("known_faces_dict.pkl", "rb") as file:
        known_faces_dict = pickle.load(file)
    print(child_image)
    # known_faces = know_faces_dict["known_faces"]
    # known_images = know_faces_dict["known_images"]

    unknown_image_path = f'static/child_image/{str(child_image)}'
    print(unknown_image_path)
    # unknown_face_encodings = face_recognition.face_encodings(unknown_image)
    if os.path.exists(unknown_image_path):
        # unknown_face_encoding = unknown_face_encodings[0]
        unknown_image = face_recognition.load_image_file(unknown_image_path)
        unknown_face_encodings = face_recognition.face_encodings(unknown_image)


        if len(unknown_face_encodings) > 0:
            unknown_face_encoding = unknown_face_encodings[0]

        match_found = False
        tolerance = 0.6  # Tolerance for face comparison

        for known_name, known_face_encoding in known_faces_dict.items():
            # Compare the unknown face to the known faces
            result = face_recognition.compare_faces([known_face_encoding], unknown_face_encoding, tolerance=tolerance)

            if result[0]:
                print(f"Successful match found: {known_name}")
                match_found = True

                # Display the matched image
                matched_image_path = os.path.join("", known_name + os.path.splitext(unknown_image_path)[1])
                matched_image = Image.open(matched_image_path)
                matched_image.show()
                destination_path = f'static/matched/{str(child_image)}'
                matched_image.save(destination_path)
                print(destination_path)
                break

            if not match_found:
                print("No match found")
                return ("")
    else:
        print("No face found in the unknown image")
        return ("")
    return (destination_path)
    
def lostchild(request):
    
    data=request.POST
    child_name=data.get('child_name')
    child_age=data.get('child_age')
    state=data.get('state')
    fir_no=data.get('fir_no')
    child_image=request.FILES.get('child_image')
    child_height=data.get('child_height')
    birth_mark=data.get('birth_mark')
    description=data.get('description')
    Lostchild.objects.create(child_name=child_name,
                         child_age=child_age,
                         state=state,
                         fir_no=fir_no,
                         child_image=child_image,
                         child_height=child_height,
                         description=description,
                         birth_mark=birth_mark)
    
    
    with open("known_faces_dict.pkl", "rb") as file:
        known_faces_dict = pickle.load(file)

    # known_faces = know_faces_dict["known_faces"]
    # known_images = know_faces_dict["known_images"]
    print(child_image)
    unknown_image_path = f'static/child_image/{child_image}'
    # unknown_face_encodings = face_recognition.face_encodings(unknown_image)
    if os.path.exists(unknown_image_path):
        # unknown_face_encoding = unknown_face_encodings[0]
        unknown_image = face_recognition.load_image_file(unknown_image_path)
        unknown_face_encodings = face_recognition.face_encodings(unknown_image)

        
        if len(unknown_face_encodings) > 0:
            unknown_face_encoding = unknown_face_encodings[0]

        match_found = False
        tolerance = 0.6  # Tolerance for face comparison

        for known_name, known_face_encoding in known_faces_dict.items():
            # Compare the unknown face to the known faces
            result = face_recognition.compare_faces([known_face_encoding], unknown_face_encoding, tolerance=tolerance)

            if result[0]:
                print(f"Successful match found: {known_name}")
                match_found = True

                # Display the matched image
                matched_image_path = os.path.join("", known_name + os.path.splitext(unknown_image_path)[1])
                matched_image = Image.open(matched_image_path)
                matched_image.show()
                destination_path = 'static/matched/matched_image.jpg'
                matched_image.save(destination_path)
                print(destination_path)
                break

            if not match_found:
                print("No match found")
                return ("")
    else:
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
    if request.method != "POST":
        return render(request,"parent_sign.html")
    data=request.POST
    first_name=data.get("first_name")
    last_name=data.get("last_name")
    username=data.get("username")
    email=data.get("email")
    password=data.get("password")
    confirm_password=data.get("confirm_password")
    if password != confirm_password:
        return HttpResponse("Password and confirm password does not match")
    if User.objects.filter(username=username).exists():
        messages.error(request,"Username already exists")
        return redirect('/parent_sign/')
    
    print(first_name)
    print(last_name)
    print(username)
    print(email)
    print(password)
    print(confirm_password)
    user=User.objects.create_user(
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        
    )
    user.set_password(password)
    user.save()
    messages.info(request,"User created successfully")
    return render(request,'parent_sign.html')
def parent_login(request):
    if request.method != "POST":
        return render(request,'parent_login.html')
    username=request.POST.get("username")
    password=request.POST.get("password")
    print(username)
    print(password)
    if not User.objects.filter(username=username).exists():
        messages.error(request,"Username doesn't exist")
        return redirect('/parent_login/')
    user=authenticate(request,username=username,password=password)
    if user is not None:
        # login(request,user)
        return redirect('/parent_dash/')

    messages.error(request,"Username or password is incorrect")
    return render(request,'parent_login.html')
def resque_sign(request):
    if request.method != "POST":
        return render(request,"resque_sign.html")
    data=request.POST
    first_name=data.get("first_name")
    last_name=data.get("last_name")
    username=data.get("username")
    email=data.get("email")
    password=data.get("password")
    confirm_password=data.get("confirm_password")
    if password != confirm_password:
        return HttpResponse("Password and confirm password does not match")
    if User.objects.filter(username=username).exists():
        messages.error(request,"Username already exists")
        return redirect('/resque_sign/')
    
    print(first_name)
    print(last_name)
    print(username)
    print(email)
    print(password)
    print(confirm_password)
    user=User.objects.create_user(
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        
    )
    user.set_password(password)
    user.save()
    messages.info(request,"User created successfully")
    return render(request,'resque_sign.html')

def resque_login(request):
    if request.method != "POST":
        return render(request,'resque_login.html')
    username=request.POST.get("username")
    password=request.POST.get("password")
    print(username)
    print(password)
    if not User.objects.filter(username=username).exists():
        messages.error(request,"Username doesn't exist")
        return redirect('/resque_login/')
    user=authenticate(request,username=username,password=password)
    if user is not None:
        # login(request,user)
        return redirect('/resque_dash/')

    messages.error(request,"Username or password is incorrect")
    return redirect('/resque_login/')
def resque_dash(request):
    match=""
    if request.method == "POST" :
        match=childdata(request)
        path = match.split("/")
        path[0] = "media"
        match="/"+"/".join(path)
        print(match)
    print(match)
    print(Child.objects.all())
    import os

# Get the full path to the static/child_image folder
    static_child_image_folder_path = os.path.join('static/child_image')

# Get a list of all the files in the static/child_image folder
    static_child_image_files = os.listdir(static_child_image_folder_path)

# Iterate over the files and delete them
    # for file in static_child_image_files:
        # os.remove(os.path.join(static_child_image_folder_path, file))


        
    if(match=="/media"):
        return render(request,'resque_dash.html' ,{'match':'/media/rimage/noimage.png','found':"Match Not Found"})
    return render(request,'resque_dash.html',{'match':match,'found':"Match Found"})

def parent_dash(request):
    match=""
    if request.method == "POST" :
        match=lostchild(request)
        path = match.split("/")
        path[0] = "media"
        match="/"+"/".join(path)
        print(f'this is {match}')
        
    print(Child.objects.all())
    if(match=="/media"):
        return render(request,'parent_dash.html' ,{'match':'/media/rimage/noimage.png','found':"Match Not Found"})
    return render(request,'parent_dash.html' ,{'match':match,'found':"Match Found",'desc':"You will get an email about the whereabouts of your child.Now please smile...."})

