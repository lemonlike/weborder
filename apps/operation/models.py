# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from users.models import UserProfile
from foods.models import Food

# Create your models here.


class UserAsk(models.Model):
    name = models.CharField(verbose_name=u"姓名", max_length=10)
    mobile = models.CharField(verbose_name=u"手机号", max_length=11)
    food_name = models.CharField(verbose_name=u"菜名", max_length=20)
    add_time = models.DateTimeField(verbose_name=u"咨询时间", default=datetime.now)

    class Meta:
        verbose_name = u"用户咨询"
        verbose_name_plural = verbose_name


class FoodComments(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    food = models.ForeignKey(Food, verbose_name=u"菜品")
    comments = models.CharField(verbose_name=u"评论内容", max_length=200)
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)

    class Meta:
        verbose_name = u"用户评论"
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    food = models.ForeignKey(Food, verbose_name=u"菜品")
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)

    class Meta:
        verbose_name = u"用户收藏"
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    name = models.IntegerField(verbose_name=u"接收用户", default=0)
    message = models.CharField(verbose_name=u"消息内容", max_length=200)
    has_read = models.BooleanField(verbose_name=u"是否已读", default=False)
    add_time = models.DateTimeField(verbose_name=u"发送时间", default=datetime.now)

    class Meta:
        verbose_name = u"用户消息"
        verbose_name_plural = verbose_name


class UserFood(models.Model):
    user_food_id = models.IntegerField(primary_key=True, verbose_name=u"点过的菜id", default=1)
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    food = models.ForeignKey(Food, verbose_name=u"菜品")

    class Meta:
        verbose_name = u"点过的菜"
        verbose_name_plural = verbose_name
