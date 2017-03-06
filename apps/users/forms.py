# -*- coding: utf-8 -*-
__author__ = 'lemon'

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5, error_messages={"invalid": u"密码长度至少为5个字符"})