# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField

from users.models import UserProfile

# Create your models here.


class Food(models.Model):
    name = models.CharField(verbose_name=u"菜名", max_length=50)
    price = models.IntegerField(verbose_name=u"价格", default=0)
    category = models.CharField(verbose_name=u"菜的类别", max_length=5,
                                choices=(("rh", u"热荤"), ("rs", u"热素"), ("lc", u"凉菜"),
                                         ("td", u"甜点"), ("zs", u"主食"), ("js", u"酒水")), default="rh")
    image = models.ImageField(verbose_name=u"图片", upload_to="food/%Y/%m", max_length=100, null=True, blank=True)
    taste = models.CharField(verbose_name=u"口味", max_length=20)
    detail = UEditorField(verbose_name=u"详细描述", width=600, height=300, imagePath="foods/ueditor/",
                          filePath="foods/ueditor/", default='')
    buy_nums = models.IntegerField(verbose_name=u"下单数", default=0)
    fav_nums = models.IntegerField(verbose_name=u"收藏数", default=0)
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)

    class Meta:
        verbose_name = u"菜单"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    has_pay = models.BooleanField(verbose_name=u"是否支付", default=False)
    total_money = models.IntegerField(verbose_name=u"总金额", default=0)
    order_time = models.DateTimeField(verbose_name=u"下单时间", default=datetime.now)
    preset_time = models.CharField(verbose_name=u"预订时间", max_length=20, default="")
    room_num = models.CharField(verbose_name=u"包间号", max_length=20, default="")

    class Meta:
        verbose_name = u"订单"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


class OrderDetail(models.Model):
    detail_id = models.IntegerField(primary_key=True, verbose_name=u"订单详情id", default=1)
    order = models.ForeignKey(Order, verbose_name=u"订单")
    food = models.ForeignKey(Food, verbose_name=u"菜单")
    quantity = models.IntegerField(verbose_name=u"数量", default=1)

    class Meta:
        verbose_name = u"订单详情"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.detail_id)


class Room(models.Model):
    name = models.CharField(verbose_name=u"包间名", max_length=20)
    category = models.CharField(verbose_name=u"种类", max_length=8,
                                choices=(("big", u"12人间"), ("middle", u"8人间"), ("small", u"6人间")))
    has_order = models.BooleanField(verbose_name=u"是否预订", default=False)
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)

    class Meta:
        verbose_name = u"包间"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class ShopCart(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    food = models.ForeignKey(Food, verbose_name=u"菜单")
    quantity = models.IntegerField(verbose_name=u"一种菜的数量", default=1)
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)

    class Meta:
        verbose_name = u"购物车"
        verbose_name_plural = verbose_name

    def augment_price(self):
        return self.food.price * self.quantity
