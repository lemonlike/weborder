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
from django.conf.urls import url, include
from django.contrib import admin
import xadmin
from django.views.static import serve

from users.views import LoginView, IndexView, RegisterView, ActiveUserView, ForgetPwdView, ResetPwdView, ModifyPwdView
from users.views import LogoutView
from .settings import MEDIA_ROOT

urlpatterns = [
    # 网站后台
    url(r'^xadmin/', xadmin.site.urls),

    # 用户注册
    url(r'register/$', RegisterView.as_view(), name="register"),

    # 用户登录
    url(r'^login/$', LoginView.as_view(), name="login"),

    # 用户登出
    url(r'^logout/$', LogoutView.as_view(), name="logout"),

    # 首页
    url(r'^$', IndexView.as_view(), name="index"),

    # 验证码
    url(r'^captcha/', include('captcha.urls')),

    # 激活用户
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),

    # 忘记密码
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),

    # 打开重置密码页面
    url(r'^reset/(?P<reset_code>.*)/$', ResetPwdView.as_view(), name="reset_pwd"),

    # 重置密码
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),

    # 配置处理上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # 富文本相关url
    url(r'^ueditor/',include('DjangoUeditor.urls')),

    # 菜单相关url配置
    url(r'^food/', include('foods.urls', namespace="food")),
]
