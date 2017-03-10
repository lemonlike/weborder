# -*- coding: utf-8 -*-
__author__ = 'lemon'

from django.conf.urls import url

from .views import UserInfoView, ImageUploadView, UpdatePwdView, SendEmailCodeView, UpdateEmailView
from .views import MyFavFoodView, MyMessageView, UserFoodView

urlpatterns = [
    # 用户基本信息
    url(r'^info/$', UserInfoView.as_view(), name="user_info"),

    # 修改用户头像
    url(r'^image/upload/$', ImageUploadView.as_view(), name="image_upload"),

    # 个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),

    # 个人中心发送修改邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name="sendemail_code"),

    # 个人中心修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),

    # 我的收藏
    url(r'^fav_food/$', MyFavFoodView.as_view(), name="fav_food"),

    # 我的消息
    url(r'^my_message/$', MyMessageView.as_view(), name="my_message"),

    # 点过的菜
    url(r'^user_food/$', UserFoodView.as_view(), name="user_food"),
]