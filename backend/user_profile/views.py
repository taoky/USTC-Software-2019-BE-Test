from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import UserProfile


# Create your views here.
def index_view(request, username):
    """
    view the profile related to a user
    :param request:
    :param username: the name of the user
    :return:
    | err_code |    err_msg     | description  | Other Properties |
    | :------: | :------------: | :----------: | :--------------: |
    |    0     |       ''       |   Success    |        -         |
    |    1     | 'No such user' | No such user |        -         |
    """
    ret_json = {
        'err_code': 0,
        'err_msg': '',
    }
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        ret_json['err_code'] = 1
        ret_json['err_msg'] = 'No such user'

        return JsonResponse(ret_json)
    else:
        profile = user.userprofile

        ret_json['email'] = profile.email
        ret_json['bio'] = profile.bio

        return JsonResponse(ret_json)


@login_required
def edit_view(request, username):
    """
    edit the profile related to a user
    you may say that parameter:username won't be needed.
    Because of course you will only edit your own profile. But
    perhaps one day the access control of this website
    is changed and superuser can do anything (though now
    they can't). Who knows.
    :param request:
    :param username: the name of the user
    :return:
    | err_code |       err_msg       |                         description                          | Other Properties |
    | :------: | :-----------------: | :----------------------------------------------------------: | :--------------: |
    |    0     |         ''          |                           Success                            |        -         |
    |    1     |   'No such user'    |                         No such user                         |        -         |
    |    2     | 'Permission denied' | You haven't logged in or you have no access to this profile. |        -         |
                                       (for example, you are a not superuser and you are trying to
                                       edit other's profile)
    """
    ret_json = {
        'err_code': 0,
        'err_msg': '',
    }

    # it's ok because login is required
    expect_username = request.user.username
    if username != expect_username:
        ret_json['err_code'] = 2
        ret_json['err_msg'] = 'Permission denied'
        return JsonResponse(ret_json)

    if request.method == 'POST':
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            ret_json['err_code'] = 1
            ret_json['err_msg'] = 'No such user'

            return JsonResponse(ret_json)
        else:
            profile = user.userprofile

            profile.email = request.POST.get('email')
            profile.bio = request.POST.get('bio')

            profile.save()

            ret_json['email'] = request.POST.get('email') or '' # prevent 'null' from json
            ret_json['bio'] = request.POST.get('bio') or ''

        return JsonResponse(ret_json)

    else:
        return JsonResponse(ret_json)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    instance.userprofile.save()



