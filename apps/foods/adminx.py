# -*- coding: utf-8 -*-
__author__ = 'lemon'

import xadmin

from .models import Food, Order, OrderDetail, Room


class FoodAdmin(object):
    list_display = ['name', 'price', 'category', 'taste', 'buy_nums', 'fav_nums', 'add_time']
    search_fields = ['name', 'price', 'category', 'taste', 'detail', 'buy_nums', 'fav_nums']
    list_filter = ['name', 'price', 'category', 'taste', 'detail', 'buy_nums', 'fav_nums', 'add_time']


class OrderAdmin(object):
    list_display = ['user', 'room_num', 'total_money', 'preset_time', 'order_time', 'has_pay']
    search_fields = ['user__username', 'room_num', 'total_money', 'has_pay']
    list_filter = ['user__username', 'room_num', 'total_money', 'preset_time', 'order_time', 'has_pay']


class OrderDetailAdmin(object):
    list_display = ['order', 'food']
    search_fields = ['order__id', 'food__name']
    list_filter = ['order__id', 'food__name']

xadmin.site.register(Food, FoodAdmin)
xadmin.site.register(Order, OrderAdmin)
xadmin.site.register(OrderDetail, OrderDetailAdmin)