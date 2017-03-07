# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password

from .models import UserProfile

# Create your views here.

from django.views.generic.base import View

from .forms import LoginForm, RegisterForm
from operation.models import UserMessage


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):
    """
    用户注册
    """
    def get(self, requst):
        register_form = RegisterForm()
        return render(requst, "register.html", {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": u"用户已存在"})
            pass_word = request.POST.get("password", '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # 写入注册欢迎消息
            user_message = UserMessage()
            user_message.name = user_profile.id
            user_message.message = u"欢迎注册在线点餐网~"
            user_message.save()
        else:
            return render(request, "register.html", {"register_form": register_form})


class LoginView(View):
    """
    用户登录
    """
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", '')
            pass_word = request.POST.get("password", '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": u"用户未激活"})
            else:
                return render(request, "login.html", {"msg": u"用户名或密码错误"})

        else:
            return render(request, "login.html", {"login_form": login_form})


class IndexView(View):
    """
    首页
    """
    def get(self, request):
        return render(request, "index.html", {})

