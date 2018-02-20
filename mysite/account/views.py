from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, views
from .forms import LoginForm, RegistrationForm, UserProfileForm

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
            return HttpResponse("successfully")
        else:
            return HttpResponse("sorry, the information is invalid")
    else:
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()  # 新增
        return render(request, 'account/register.html', {'form': user_form, "profile":userprofile_form})
