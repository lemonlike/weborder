# -*- coding: utf-8 -*-
__author__ = 'lemon'

from django.conf.urls import url

from .views import FoodListView, FoodDetailView, AddFavView, AddCommentsView, AddShopCartView, ShopCartView
from .views import ConfirmOrder, CompletePayView, MyOrderView, MyOrderDetail


urlpatterns = [
    # 菜单列表页
    url(r'^list/$', FoodListView.as_view(), name="food_list"),

    # 菜品详情页
    url(r'^detail/(?P<food_id>\d+)/$', FoodDetailView.as_view(), name="food_detail"),

    # 用户收藏
    url(r'add_fav/$', AddFavView.as_view(), name="add_fav"),

    # 添加课程评论
    url(r'^add_comment/$', AddCommentsView.as_view(), name="add_comment"),

    # 加入购物车
    url(r'^cart_add/(?P<food_id>\d+)/$', AddShopCartView.as_view(), name="cart_add"),

    # 购物车页面
    url(r'^shop_cart/$', ShopCartView.as_view(), name="shop_cart"),

    # 确认订单
    url(r'^confirm_order/$', ConfirmOrder.as_view(), name="confirm_order"),

    # 完成支付
    url(r'^complete_pay/$', CompletePayView.as_view(), name="complete_pay"),

    # 我的订单
    url(r'^my_order/$', MyOrderView.as_view(), name="my_order"),

    # 订单详情
    url(r'^my_order_detail/(?P<order_id>\d+)/$', MyOrderDetail.as_view(), name="order_detail"),
]