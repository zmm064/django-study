from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

# from django.conf import settings

urlpatterns = [
    # url(r'^login/$', views.user_login, name="user_login"),
    url(r'^login/$', auth_views.login, {"template_name": "account/login.html"}, name="user_login"),
    url(r'^logout/$', auth_views.logout, {"template_name": "account/logout.html"}, name="user_logout"),
    url(r'^register/$', views.register, name="user_register"),


    url(r'^password-change/$', auth_views.password_change, 
        {"post_change_redirect":"/account/password-change-done"}, name='password_change'),
    url(r'^password-change-done/$', auth_views.password_change_done, name='password_change_done'),
    # 向用户发送邮件
    url(r'^password-reset/$', auth_views.password_reset,  
        {"template_name":"account/password_reset_form.html",  # 发送邮件的表单模板
         "email_template_name":"account/password_reset_email.html", # 发送给用户的邮件内容
         "subject_template_name":"account/password_reset_subject.txt",  # 所发邮件的主题
         "post_reset_redirect":"/account/password-reset-done"},  # 在URL中声明转向的目标路径
         name="password_reset"),

    # 显示发送成功的信息
    url(r'^password-reset-done/$', auth_views.password_reset_done,
        {"template_name":"account/password_reset_done.html"}, name="password_reset_done"),
    # 查看邮件，并点击邮件中的链接，让用户输入新的密码
    url(r'^password-reset-confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', auth_views.password_reset_confirm,  
        {"template_name":"account/password_reset_confirm.html", 
         "post_reset_redirect":"/account/password-reset-complete"}, 
         name="password_reset_confirm"),
    # 显示成功的信息
    url(r'^password-reset-complete/$', auth_views.password_reset_complete, 
        {"template_name":"account/password_reset_complete.html"},  # 显示密码重置成功的信息
        name="password_reset_complete"),
]