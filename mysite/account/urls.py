from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

# from django.conf import settings

urlpatterns = [
    # url(r'^login/$', views.user_login, name="user_login"),
    url(r'^login/$', auth_views.login, {"template_name": "account/login.html"}, name="user_login"),
]