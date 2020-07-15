from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from .form import UserLoginForm,UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .form import ProfileForm
from .models import Profile
# Create your views here.

def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # .cleand_data 清洗出合法数据
            data = user_login_form.cleaned_data
            # 检验账号/密码是否正确匹配数据库总的某个用户
            # 如果均匹配返回这个用户
            user = authenticate(username=data['username'],password=data['password'])
            if user:
                # 将用户数据保存在session中,即实现了登录动作
                login(request, user)
                return redirect('body:index')
            else:
                return HttpResponse('账号或者密码输入有误,请重新输入')
        else:
            return HttpResponse('账号密码不合法')
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form':user_login_form}
        return render(request, 'userprofile/login.html',context)
    else:
        return HttpResponse('请使用GET或POST请求数据')


def user_logout(request):
    logout(request)
    return redirect('body:index')


def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            # 保存好数后立即登录并返回博客列表页面
            login(request, new_user)
            return redirect('body:list')
        else:
            return HttpResponse('注册输入有误,请重新输入')
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, 'userprofile/register.html', context=context)
    else:
        return HttpResponse('请使用GET或POST请求数据')


# 用户删除
@login_required(login_url='/userprofile/login/')
def user_delete(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        # 验证登录用户,带删除用户是否相同
        if request.user == user:
            logout(request)
            user.delete()
            return redirect('user:login')
        else:
            return HttpResponse('你没有删除权限')
    else:
        return HttpResponse('仅接受POST请求')


# 编辑用户信息
@login_required(login_url='/userprofile/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    # user_id shi OneToOneField自动生成的字段
    # profile = Profile.objects.get(user_id=id)
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)
    if request.method == 'POST':
        # 验证修改数据这,是否是本人
        if request.user != user:
            return HttpResponse('你没有权限修改次用户信息')
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            # 获得清洗后的合法数据
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd['phone']
            profile.slogan = profile_cd['slogan']
            if 'avatar' in request.FILES:
                profile.avatar = profile_cd['avatar']
            profile.save()
            return redirect('userprofile:profile_eidt', id=id)
        else:
            return HttpResponse('注册表单输入有误')
    elif request.method == 'GET':
        profile_form = ProfileForm()
        profile = Profile.objects.get(id=id)
        context = {'profile_form':profile_form,'profile':profile}
        return render(request, 'userprofile/edit.html', context=context)
    else:
        return HttpResponse('请使用GET或者POST请求数据')