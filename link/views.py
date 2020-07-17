from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Link
from .form import LinkForm
# Create your views here.


def link(request):
        links = Link.objects.all()
        context = {'links': links,'message': '欢迎友友ヽ(￣ω￣(￣ω￣〃)ゝ'}
        return render(request, 'link/list.html',context=context)

def add_link(request):
    if request.method == 'POST':
        link_form = LinkForm(request.POST,request.FILES)
        if link_form.is_valid():
            link = link_form.save(commit=False)
            link.name = link_form.cleaned_data['name']
            link.url = link_form.cleaned_data['url']
            if 'avatar' in request.FILES:
                link.avatar = link_form.cleaned_data['avatar']
            link.save()
            return redirect('links:link_form')
        else:
            links = Link.objects.all()
            context = {'links':links,'message':"友友,表单信息有误!"}
            return render(request,'link/list.html',context=context)
    else:
        return HttpResponse("仅支持POST访问")

