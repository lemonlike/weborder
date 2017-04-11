# -*- coding: utf-8 -*-
__author__ = 'lemon'

import xadmin

from .models import Food, Order, OrderDetail, Room, ShopCart


class FoodAdmin(object):
    list_display = ['name', 'price', 'category', 'taste', 'buy_nums', 'fav_nums', 'add_time']
    search_fields = ['name', 'price', 'category', 'taste', 'detail', 'buy_nums', 'fav_nums']
    list_filter = ['name', 'price', 'category', 'taste', 'detail', 'buy_nums', 'fav_nums', 'add_time']
    style_fields = {"detail": "ueditor"}
    model_icon = 'fa fa-book'
    readonly_fields = ['buy_nums', 'fav_nums']


class OrderAdmin(object):
    list_display = ['id', 'user', 'room_num', 'total_money', 'preset_time', 'order_time', 'has_pay', 'order_status']
    search_fields = ['id', 'user__username', 'room_num', 'total_money', 'has_pay']
    list_filter = ['id', 'user__username', 'room_num', 'total_money', 'preset_time', 'order_time', 'has_pay']
    refresh_times = [3, 5]
    model_icon = 'fa fa-file'
    list_editable = ['order_status']


class OrderDetailAdmin(object):
    list_display = ['order', 'food', 'quantity']
    search_fields = ['detail_id', 'order__id', 'food__name']
    list_filter = ['detail_id', 'order__id', 'food__name']
    model_icon = 'fa fa-file-text'


class RoomAdmin(object):
    list_display = ['name', 'category', 'has_order', 'add_time']
    search_fields = ['name', 'category', 'has_order']
    list_filter = ['name', 'category', 'has_order', 'add_time']
    model_icon = 'fa fa-university'


class ShopCartAdmin(object):
    list_display = ['user', 'food', 'quantity', 'add_time']
    search_fields = ['user__username', 'food__name']
    list_filter = ['user__username', 'food__name']
    model_icon = 'fa fa-cart-plus'

xadmin.site.register(Food, FoodAdmin)
xadmin.site.register(Order, OrderAdmin)
xadmin.site.register(OrderDetail, OrderDetailAdmin)
xadmin.site.register(Room, RoomAdmin)
xadmin.site.register(ShopCart, ShopCartAdmin)