# -*- coding: utf-8 -*-
__author__ = 'lemon'

from django.conf.urls import url

from .views import FoodListView, FoodDetailView, AddFavView


urlpatterns = [
    # 菜单列表页
    url(r'^list/$', FoodListView.as_view(), name="food_list"),

    # 菜品详情页
    url(r'^detail/(?P<food_id>\d+)/$', FoodDetailView.as_view(), name="food_detail"),

    # 用户收藏
    url(r'add_fav/$', AddFavView.as_view(), name="add_fav"),
]