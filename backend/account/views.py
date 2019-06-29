from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib import auth
from .forms import RegistrationForm
from .models import User_Info

#Using User_Info from models.py instead of User

def regist(request):
    """
        All the information about registration format is in the forms.py file.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            profile = request.POST['profile']
            #Using User method to create a new account
            user = User_Info.objects.create_user(username=username, password=password, profile=profile)
            return JsonResponse({"err_code":"000", "err_msg":"Registration is successful!"})
        else:
            errors = list(form.errors.values())
            err = list(errors[0])[0].split(',')
            #Using list to change ErrorList object into list object
            return JsonResponse({"err_code":err[0], "err_msg":err[1]})
    else:
        return JsonResponse({"err_code":"4.3", "err_msg":"Please use 'POST' method."})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #Check the existence of the username
        user = User_Info.objects.filter(username=username)
        if not user:
            return JsonResponse({"err_code":"101", "err_msg":"Your username does not exist!"})
        else:
            if request.user.is_authenticated:
                #Check the status of the current username, the user that already logged in can't do this again.
                return JsonResponse({"err_code":"102", "err_msg":"You have already logged in!"})
            else:
                #Using auth mod to check
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    auth.login(request, user)
                    return JsonResponse({"err_code":"100", "err_msg":"Login successfully!"})
                else:
                    return JsonResponse({"err_code":"103", "err_msg":"Wrong password!"})
    else:
        return JsonResponse({"err_code":"4.3", "err_msg":"Please use 'POST' method."})

def logout(request):
    #for user in User_Info.objects.all():
        #user.delete()
        #This is for delete data in the list
    if request.method == 'POST':
        username = request.POST['username']
        user = User_Info.objects.filter(username=username)
        if not user:
            return JsonResponse({"err_code":"201", "err_msg":"Your username does not exist!"})
            #This may not happen in practice.
        else:
            if request.user.is_authenticated:
                #Check the status of the current username, only the user that already logged in can logout.
                auth.logout(request)
                return JsonResponse({"err_code":"200", "err_msg":"Logout successfully!"})
            else:
                return JsonResponse({"err_code":"202", "err_msg":"You have to login."})
    else:
        return JsonResponse({"err_code":"4.3", "err_msg":"Please use 'POST' method."})

def profile_show(request):
    if request.method == 'POST':
        username = request.POST['username']
        user = User_Info.objects.filter(username=username)
        if not user:
            return JsonResponse({"err_code":"301", "err_msg":"Your username does not exist!"})
            #This may not happen in practice.
        else:
            if request.user.is_authenticated:
                #Check the status of the current username, only the user that already logged in can see the profile.
                user_in = User_Info.objects.get(username=username)
                profile_stuff = user_in.profile
                if len(profile_stuff) == 0:
                    return JsonResponse({"err_code":"300", "err_msg":"Profile displayed successful: You don't have any profile to show."})
                else:
                    return JsonResponse({"err_code":"300", "err_msg":str.format("Profile displayed successful, your profile is: {0}", profile_stuff)})
            else:
                return JsonResponse({"err_code":"302", "err_msg":"You have to login."})
    else:
        return JsonResponse({"err_code":"4.3", "err_msg":"Please use 'POST' method."})

def profile_update(request):
    if request.method == 'POST':
        username = request.POST['username']
        user = User_Info.objects.filter(username=username)
        if not user:
            return JsonResponse({"err_code":"401", "err_msg":"Your username does not exist!"})
        else:
            if request.user.is_authenticated:
                #Check the status of the current username, only the user that already logged in can edit the profile.
                profile_new = request.POST['profile']
                #On this situation the profile in the POST means the changed profile.
                User_Info.objects.filter(username=username).update(profile=profile_new)
                return JsonResponse({"err_code":"400", "err_msg":"Profile updated successful."})
            else:
                return JsonResponse({"err_code":"402", "err_msg":"You have to login."})
    else:
        return JsonResponse({"err_code":"4.3", "err_msg":"Please use 'POST' method."})


