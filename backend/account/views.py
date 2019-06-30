from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from .forms import RegistrationForm, MessageForm
from .models import User_Info
import datetime

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
            try:
                profile = request.POST['profile']
            except:
                return JsonResponse({"err_code":"008", "err_msg":"You must add profile into request."})
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
        try:
            username = request.POST['username']
            password = request.POST['password']
        except:
            return JsonResponse({"err_code":"104", "err_msg":"You must add username and password into request."})
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
        try:
            username = request.POST['username']
        except:
            return JsonResponse({"err_code":"203", "err_msg":"You must add username into request."})
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
        try:
            username = request.POST['username']
        except:
            return JsonResponse({"err_code":"303", "err_msg":"You must add username into request."})
        user = User_Info.objects.filter(username=username)
        if not user:
            return JsonResponse({"err_code":"301", "err_msg":"Your username does not exist!"})
            #This may not happen in practice.
        else:
            if request.user.is_authenticated:
                #Check the status of the current username, only the user that already logged in can see the profile.
                user_in = User_Info.objects.get(username=username)
                profile_info = user_in.profile
                if len(profile_info) == 0:
                    return JsonResponse({"err_code":"300", "err_msg":"Profile displayed successful: You don't have any profile to show."})
                else:
                    return JsonResponse({"err_code":"300", "err_msg":str.format("Profile displayed successful, your profile is: {0}", profile_info)})
            else:
                return JsonResponse({"err_code":"302", "err_msg":"You have to login."})
    else:
        return JsonResponse({"err_code":"4.3", "err_msg":"Please use 'POST' method."})

def profile_update(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
        except:
            return JsonResponse({"err_code":"403", "err_msg":"You must add username into request."})
        user = User_Info.objects.filter(username=username)
        if not user:
            return JsonResponse({"err_code":"401", "err_msg":"Your username does not exist!"})
        else:
            if request.user.is_authenticated:
                #Check the status of the current username, only the user that already logged in can edit the profile.
                try:
                    profile_new = request.POST['profile']
                except:
                    return JsonResponse({"err_code":"404", "err_msg":"you must add profile into request."})
                #On this situation the profile in the POST means the changed profile.
                User_Info.objects.filter(username=username).update(profile=profile_new)
                return JsonResponse({"err_code":"400", "err_msg":"Profile updated successful."})
            else:
                return JsonResponse({"err_code":"402", "err_msg":"You have to login."})
    else:
        return JsonResponse({"err_code":"4.3", "err_msg":"Please use 'POST' method."})

def message_create(request):
    """
        Using username to save message_id,
        That's to say you don't have to login to create a message.
    """
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            wait_time_str = request.POST['wait_time']
            message_id_str = request.POST['username']
            try:
                message = request.POST['message']
            except:
                return JsonResponse({"err_code":"507", "err_msg":"You must add message into request."})
            release_time = datetime.datetime.now()
            release_time_str = release_time.strftime("%Y-%m-%d-%H-%M-%S")
            show_time = release_time + datetime.timedelta(minutes=int(wait_time_str))
            show_time_str = show_time.strftime("%Y-%m-%d-%H-%M-%S")
            message_new = User_Info.objects.create_user(username=message_id_str, release_time=release_time_str, message=message, wait_time=wait_time_str, show_time=show_time_str)
            #Using User method to create a new account.
            #Cause it requires a username, so just use the message_id to represent it.
            return JsonResponse({"err_code":"500", "err_msg":"Message create successfully!"})
        else:
            errors = list(form.errors.values())
            err = list(errors[0])[0].split(',')
            #Using list to change ErrorList object into list object
            return JsonResponse({"err_code":err[0], "err_msg":err[1]})
    else:
        return JsonResponse({"err_code":"4.3", "err_msg":"Please use 'POST' method."})

def message_show(request):
    if request.method == 'POST':
        msg_id_list = User_Info.objects.all().values_list('username')
        if not msg_id_list:
            return JsonResponse({"err_code":"601", "err_msg":"You don't have any messages to show."})
        else:
            msg_to_show = []
            msg_all = ""
            for msg_id in msg_id_list:
                msg_id = msg_id[0]
                if len(msg_id) < 3:
                    msg_in = User_Info.objects.get(username=msg_id)
                    time_now = datetime.datetime.now()
                    show_time_str = msg_in.show_time
                    show_time = datetime.datetime.strptime(show_time_str, "%Y-%m-%d-%H-%M-%S")
                    if time_now >= show_time:
                        message_info = msg_in.message
                        release_time_info = msg_in.release_time
                        msg_all_info = str.format("Message id: {0}. Your message is: {1}. Your message was created at: {2}.\n", int(msg_id), message_info, release_time_info)
                    else:
                        message_info = "You can't see this message now!"
                        msg_all_info = str.format("Message id: {0}. {1} You can see this message at: {2}.\n", int(msg_id), message_info, show_time_str)
                    msg_to_show.append(msg_all_info)
                else:
                    continue
            for msg in msg_to_show:
                msg_all = msg_all + msg
            #return HttpResponse(msg_all)
            return JsonResponse({"err_code":"600", "err_msg":msg_all})
    else:
        return JsonResponse({"err_code":"4.3", "err_msg":"Please use 'POST' method."})

def message_delete(request):
    if request.method == 'POST':
        try:
            message_id_str = request.POST['username']
        except:
            return JsonResponse({"err_code":"702", "err_msg":"You must add username(message_id) into request."})
        msg = User_Info.objects.filter(username=message_id_str)
        if not msg:
            return JsonResponse({"err_code":"701", "err_msg":"This message_id does not exist!"})
        else:
            User_Info.objects.filter(username=message_id_str).delete()
            return JsonResponse({"err_code":"700", "err_msg":"This message deletes successfully!"})
    else:
        return JsonResponse({"err_code":"4.3", "err_msg":"Please use 'POST' method."})
