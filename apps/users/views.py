# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password
from django.views.generic.base import View
import json
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import UserProfile
from utils.mixin_utils import LoginRequiredMixin
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyForm, UserInfoForm, ImageUploadForm
from operation.models import UserMessage, UserFavorite, UserFood
from utils.email_send import send_email
from .models import EmailVerifyRecord, Banner
from foods.models import Food


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
            user_email = request.POST.get("email", '')
            if UserProfile.objects.filter(email=user_email):
                return render(request, "register.html", {"register_form": register_form, "msg": u"用户已存在"})
            pass_word = request.POST.get("password", '')
            user_profile = UserProfile()
            user_profile.username = user_email
            user_profile.email = user_email
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # 写入注册欢迎消息
            user_message = UserMessage()
            user_message.name = user_profile.id
            user_message.message = u"欢迎注册在线点餐网~"
            user_message.save()

            send_email(user_email, "register")
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


class ActiveUserView(View):
    """
    用户激活
    """
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        # return render(request, "login.html")
        return HttpResponseRedirect(reverse("login"))


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


class LogoutView(View):
    """
    用户登出
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class IndexView(View):
    """
    首页
    """
    def get(self, request):
        all_banners = Banner.objects.all().order_by("index")
        foods = Food.objects.all().order_by("-fav_nums")[:8]
        banner_foods = Food.objects.all().order_by("-buy_nums")[:3]

        return render(request, "index.html", {
            "all_banners":all_banners,
            "foods": foods,
            "banner_foods": banner_foods
        })


class ForgetPwdView(View):
    """
    忘记密码
    """
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", '')
            if UserProfile.objects.filter(email=email):
                send_email(email, "forget")
                return render(request, "send_success.html")
            else:
                return render(request, "forgetpwd.html", {"forget_form": forget_form, "msg": u"该用户不存在"})
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})


class ResetPwdView(View):
    """
    打开重置密码页面
    """
    def get(self, requset, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(requset, "password_reset.html", {"email": email})
        else:
            return render(requset, "active_fail.html")


class ModifyPwdView(View):
    """
    重置密码
    """
    def post(self, request):
        modify_form = ModifyForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", '')
            pwd2 = request.POST.get("password2", '')
            email = request.POST.get("email", '')
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"msg": u"密码不一致，请重新输入！", "email": email})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", '')
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})


class UserInfoView(LoginRequiredMixin, View):
    """
    个人信息的显示及修改
    """
    def get(self, request):
        return render(request, "usercenter-info.html")

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            request.user.save()
            return HttpResponse('{"status": "success"}', content_type="application/json")
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type="application/json")


class ImageUploadView(LoginRequiredMixin, View):
    """
    修改头像
    """
    def post(self, request):
        image_form = ImageUploadForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            request.user.save()
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail"}', content_type="application/json")


class UpdatePwdView(LoginRequiredMixin, View):
    """
    个人中心修改密码
    """
    def post(self, request):
        modify_form = ModifyForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", '')
            pwd2 = request.POST.get("password2", '')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')

            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')

        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """
    def get(self, request):
        email = request.GET.get("email", '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')

        send_email(email, "update_email")
        return HttpResponse('{"status": "success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """
    个人中心修改邮箱验证码
    """
    def post(self,request):
        email = request.POST.get("email", '')
        code = request.POST.get("code", '')

        existed_records = EmailVerifyRecord.objects.filter(code=code, email=email, send_type="update_email")
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码错误"}', content_type='application/json')


class MyFavFoodView(LoginRequiredMixin, View):
    """
    我的收藏
    """
    def get(self, request):
        fav_foods = UserFavorite.objects.filter(user=request.user)
        return render(request, "usercenter-fav-course.html", {
            "fav_foods": fav_foods
        })


class MyMessageView(LoginRequiredMixin, View):
    """
    我的消息
    """
    def get(self, request):
        user_messages = UserMessage.objects.filter(name=request.user.id)

        # 对用户消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(user_messages, 5, request=request)
        messages = p.page(page)
        return render(request, "usercenter-message.html", {
            "all_messages": messages
        })


class UserFoodView(LoginRequiredMixin, View):
    """
    点过的菜
    """
    def get(self, request):
        user_foods = UserFood.objects.filter(user=request.user)
        return render(request, "usercenter-userfood.html", {"user_foods": user_foods})

