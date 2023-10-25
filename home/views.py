from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import User
from .forms import UserRegistrationForm  # Import your UserRegistrationForm here

def home(request):
    image_files = []  # Assuming this part works as expected
    count = 0
    for image_file in os.listdir('static/banner'):
        image_files.append('media/banner/' + image_file)
        count += 1
    context = {
        'image_files': image_files,
        'count': range(0, count),
    }
    print(count)
    return render(request, 'index.html', context)

def parent_sign(request):
    return render(request, 'parent_sign.html')

def parent_login(request):
    return render(request, 'parent_login.html')

def resque_sign(request):
    if request.method == 'POST':
        full_name = request.POST.get('fullname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Your password and confirm password do not match")
        else:
            if User.objects.filter(Q(username=username) | Q(email=email)).exists():
                messages.error(request, "Username or email already exists")
            else:
                my_user = User.objects.create_user(username=username, email=email, password=password)
                my_user.full_name = full_name  # Set the user's full name
                my_user.save()
                messages.success(request, "Your account has been successfully created")
                return redirect('resque_login')

    # View logic for the signup page
    return render(request, 'resque_sign.html')

def resque_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('resque_dash')  # Assuming you want to redirect to 'resque_dash' on successful login
        else:
            messages.error(request, "Invalid username or password")

    # View logic for the login page
    return render(request, 'resque_login.html')

@login_required(login_url='resque_login')
def resque_dash(request):
    # View logic for the dashboard page
    return render(request, 'resque_dash.html')

def user_logout(request):
    logout(request)
    return redirect('index')  # Redirect to 'index' or any other page you prefer

# Add your UserRegistrationForm logic here
def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user data to the database
            return redirect('resque_login')  # Redirect to a success page
    else:
        form = UserRegistrationForm()

    return render(request, 'resque_sign.html', {'form': form})
