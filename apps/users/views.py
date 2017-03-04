# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.

from django.views.generic.base import View


class LoginView(View):
    """
    用户登录
    """
    def get(self, request):
        return render(request, "login.html")


class IndexView(View):
    """
    首页
    """
    def get(self, request):
        return render(request, "index.html", {})

