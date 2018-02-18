from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm

def user_login(request):
    if request.method == "POST":  # 返回HTTP请求类型的字符串
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            # 检验此用户是否为本网站项目的用户，及其密码是否正确。
            # 正确则返回用户实例，错误则返回None
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                # 以User实例对象作为参数，实现用户登录
                login(request, user)
                # 用户登录之后，Django会自动调用默认的session应用，
                # 将用户ID保存在session中，完成用户登录操作
                return HttpResponse("Wellcom You. You have been authenticated succefully")
            else:
                return HttpResponse("Sorry. Your username or password is not right")
        else:
            return HttpResponse("Invalid Login")
    if request.method == "GET":
        login_form = LoginForm()
        return render(request, "account/login.html", {'form': login_form})
