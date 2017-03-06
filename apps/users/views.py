# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import UserProfile

# Create your views here.

from django.views.generic.base import View

from .forms import LoginForm


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):
    def get(self, requst):

        return render(requst, "register.html", {})


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

