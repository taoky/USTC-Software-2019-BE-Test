from django.shortcuts import render
from .models import Detail
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import DetailForm

# Create your views here.
def index(request):
    """个人主页"""
    return render(request, 'accounts/index.html')

def details(request):
    """显示所有个人信息名称"""
    details = Detail.objects.all()
    context = {'details': details}
    return render(request, 'accounts/details.html', context)

def detail(request, detail_id):
    """显示单项信息及细节"""
    detail = Detail.objects.get(id=detail_id)
    information = detail.information_set.all()
    context = {'detail': detail, 'information': information}
    return render(request, 'accounts/detail.html', context)

def new_detail(request):
    """添加新信息名"""
    """未提交数据：创建一个新表单"""
    """POST提交的数据，对数据进行处理"""
    if request.method != 'POST':
        form = DetailForm()
    else:
        form = DetailForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('accounts:details'))

    context = {'form': form}
    return render(request, 'accounts/new_detail.html', context)


