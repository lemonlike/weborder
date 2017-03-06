# -*- coding: utf-8 -*-
"""weborder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
import xadmin

from users.views import LoginView, IndexView, RegisterView

urlpatterns = [
    # 网站后台
    url(r'^xadmin/', xadmin.site.urls),

    # 用户注册
    url(r'register/$', RegisterView.as_view(), name="register"),

    # 用户登录
    url(r'^login/$', LoginView.as_view(), name="login"),

    # 首页
    url(r'^$', IndexView.as_view(), name="index"),
]
