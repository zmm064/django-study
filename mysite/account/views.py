from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, views
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, RegistrationForm, UserProfileForm, UserInfoForm, UserForm
from .models import UserProfile, UserInfo
from django.contrib.auth.models import User

#def user_login(request):
#    if request.method == "POST":  # 返回HTTP请求类型的字符串
#        login_form = LoginForm(request.POST)
#        if login_form.is_valid():
#            cd = login_form.cleaned_data
#            # 检验此用户是否为本网站项目的用户，及其密码是否正确。
#            # 正确则返回用户实例，错误则返回None
#            user = authenticate(username=cd['username'], password=cd['password'])
#            if user:
#                # 以User实例对象作为参数，实现用户登录
#                login(request, user)
#                # 用户登录之后，Django会自动调用默认的session应用，
#                # 将用户ID保存在session中，完成用户登录操作
#                return HttpResponse("Wellcom You. You have been authenticated succefully")
#            else:
#                return HttpResponse("Sorry. Your username or password is not right")
#        else:
#            return HttpResponse("Invalid Login")
#    if request.method == "GET":
#        login_form = LoginForm()
#        return render(request, "account/login.html", {'form': login_form})

def register(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)  # 新增
        if user_form.is_valid() & userprofile_form.is_valid():
            # 为什么不直接保存到数据库, 是因为此时保存的数据中没有密码吗
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # 同时保存两张表
            new_profile = userprofile_form.save(commit=False)  # 新增
            new_profile.user = new_user  # 新增
            new_profile.save()  # 新增
            # 保存第三张表
            UserInfo.objects.create(user=new_user)
            return HttpResponse("successfully")
        else:
            return HttpResponse("sorry, the information is invalid")
    else:
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()  # 新增
        return render(request, 'account/register.html', {'form': user_form, "profile":userprofile_form})


@login_required(login_url="/account/login/")
def myself(request):
    # 获取登录用户的个人信息
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user)
    return render(request, "account/myself.html", {"user":user, "userinfo":userinfo, "userprofile":userprofile})


@login_required(login_url='/account/login/')
def myself_edit(request):
    # 获取登录用户的个人信息
    #user = User.objects.get(username=request.user.username)
    user = request.user
    userprofile = UserProfile.objects.get(user=request.user)
    userinfo = UserInfo.objects.get(user=request.user)

    if request.method == "POST":
        # 从用户提交的表单中获取信息
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid() * userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            print(user_cd["email"])
            # 将用户表单中的信息更新到用户个人信息中
            user.email = user_cd['email']
            userprofile.birth = userprofile_cd['birth']
            userprofile.phone = userprofile_cd['phone']
            userinfo.school = userinfo_cd['school']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
            # 保存用户个人信息
            user.save()
            userprofile.save()
            userinfo.save()
        return HttpResponseRedirect('/account/my-information/')
    else:
        # 将用户的个人信息填充到表单中
        user_form = UserForm(instance=request.user)
        userprofile_form = UserProfileForm(initial={"birth":userprofile.birth, "phone":userprofile.phone})
        userinfo_form = UserInfoForm(initial={"school":userinfo.school, "company":userinfo.company, "profession":userinfo.profession, "address":userinfo.address, "aboutme":userinfo.aboutme})
        return render(request, "account/myself_edit.html", {"user_form":user_form, "userprofile_form":userprofile_form, "userinfo_form":userinfo_form})