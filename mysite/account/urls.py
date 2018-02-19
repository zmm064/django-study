from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

# from django.conf import settings

urlpatterns = [
    # url(r'^login/$', views.user_login, name="user_login"),
    url(r'^login/$', auth_views.login, {"template_name": "account/login.html"}, name="user_login"),
    url(r'^logout/$', auth_views.logout, {"template_name": "account/logout.html"}, name="user_logout"),
    url(r'^register/$', views.register, name="user_register"),
]