from django.shortcuts import render
from .models import Detail
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .forms import DetailForm, InformationForm
from .models import Detail, Information
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    """个人主页"""
    return render(request, 'accounts/index.html')

@login_required
def details(request):
    """显示所有个人信息名称"""
    if request.method != 'POST':
         return JsonResponse({"err_code": "4.3", "err_msg": "Please use 'POST' method."})
    else:
        details = Detail.objects.filter(owner=request.user).all()
        details = Detail.objects.all()
        context = {'details': details}
        return JsonResponse({"err_code":"400", "err_msg": context})

@login_required
def detail(request, detail_id):
    """显示单项信息及细节"""
    if request.method != 'POST':
         return JsonResponse({"err_code": "4.3", "err_msg": "Please use 'POST' method."})
    else:
        detail = Detail.objects.get(id=detail_id)
        if detail.owner != request.user:
            return JsonResponse({"err_code": "500", "err_msg": "wrong user"})
        informations = detail.information_set.all()
        context = {'detail': detail, 'informations': informations}
        return JsonResponse({"err_code": "501", "err_msg": context})

@login_required
def new_detail(request):
    """添加新信息名"""
    """未提交数据：创建一个新表单"""
    """POST提交的数据，对数据进行处理"""
    if request.method != 'POST':
        return JsonResponse({"err_code": "4.3", "err_msg": "Please use 'POST' method."})
    else:
        form = DetailForm(request.POST)
        if form.is_valid():
            new_detail = form.save(commit=False)
            new_detail.owner = request.user
            new_detail.save()
            return JsonResponse({"err_code": "600", "err_msg": "add successfully!"})
        else:
            return JsonResponse({"err_code": "601", "err_msg": "invalid"})

@login_required
def new_information(request, detail_id):
    """在特定主题中添加新条目"""
    """未提交数据：创建一个新表单"""
    """POST提交的数据，对数据进行处理"""
    detail= Detail.objects.get(id=detail_id)

    if request.method != 'POST':
        return JsonResponse({"err_code": "4.3", "err_msg": "Please use 'POST' method."})
    else:
        form = InformationForm(data=request.POST)
        if form.is_valid():
            new_information = form.save(commit=False)
            new_information.title = detail
            new_information.save()
            return JsonResponse({"err_code": "700", "err_msg": "add successfully!"})
        else:
            return JsonResponse({"err_code": "701", "err_msg": "Fail"})

@login_required
def edit_information(request, information_id):
    """编辑既有信息"""
    information = Information.objects.get(id=information_id)
    detail = information.title
    if detail.owner != request.user:
        return JsonResponse({"err_code": "800", "err_msg": "wrong user!"})

    if request.method != 'POST':
        return JsonResponse({"err_code": "4.3", "err_msg": "Please use 'POST' method."})
    else:
        form = InformationForm(instance=information, data=request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"err_code": "801", "err_msg": "edit successfully!"})
        else:
            return JsonResponse({"err_code": "802", "err_msg": "invalid"})

