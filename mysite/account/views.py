from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import RegisForm, UserProForm, UserForm
from django.contrib.auth.decorators import login_required
from .models import UserPro


def register(request):
    if request.method == 'POST':
        user_form = RegisForm(request.POST)
        userpro_form = UserProForm(request.POST)
        if user_form.is_valid() and userpro_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_pro = userpro_form.save(commit=False)
            new_pro.user = new_user
            new_pro.save()
            return HttpResponseRedirect(reverse('account:login'))
        else:
            return HttpResponse('fail')
    else:
        user_form = RegisForm()
        userpro_form = UserProForm()
        return render(request, 'account/register.html', {'form': user_form, 'proform': userpro_form})


@login_required(login_url='/account/login/')
def self(request):
    userpro = UserPro.objects.get(user=request.user) if hasattr(request.user, 'userpro') else UserPro.objects.create(user=request.user)
    return render(request, 'account/myself.html', {'user': request.user, 'proform': userpro})


@login_required(login_url='/account/login/')
def myself_edit(request):
    userpro = UserPro.objects.get(user=request.user)
    if request.method == "POST":
        user_form = UserForm(request.POST)
        userprofile_form = UserProForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid():
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            request.user.email = user_cd['email']
            userpro.company = userprofile_cd['company']
            userpro.selfpro = userprofile_cd['selfpro']
            userpro.phone = userprofile_cd['phone']
            request.user.save()
            userpro.save()
        return HttpResponseRedirect(reverse('account:self'))
    else:
        user_form = UserForm(instance=request.user)
        userprofile_form = UserProForm()
        return render(request, "account/myself_edit.html", {"user_form": user_form, "userprofile_form": userprofile_form})
