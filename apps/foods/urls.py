# -*- coding: utf-8 -*-
__author__ = 'lemon'

from django.conf.urls import url

from .views import FoodListView


urlpatterns = [
    # 菜单列表页
    url(r'^list/$', FoodListView.as_view(), name="food_list"),
]