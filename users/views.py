from django.shortcuts import render
from .forms import LoginForm, userRegistrationForm
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import UserEditForm, ProfileEditForm

# Login function
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Clean data 
            data = form.cleaned_data
            # Authentification 
            user = authenticate(request,username=data['username'],password=data['password'])
            if user is not None:
                login(request,user)
                return HttpResponse("User authenticated and logged in")
            else:
                return HttpResponse("Invalid Credentials")
    else:
        form = LoginForm()
    return render(request,'users/login.html',{'form':form })

# Protect the view
@login_required
def index(request):
    return render(request,'users/index.html')


# User registration
def register(request):
    if request.method =='POST':
        user_form = userRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False) # Commit = False --> without saving password
            # Clean password
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # Create Profile
            Profile.objects.create(user=new_user)
            return render(request,'users/register_done.html')
    else:
        user_form = userRegistrationForm()
    return render(request,'users/register.html',{'user_form':user_form})

# Edit Profile &  User
@login_required
def edit(request):
    if request.method =='POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)    
    return render(request,'users/edit.html',{'user_form':user_form,'profile_form':profile_form})