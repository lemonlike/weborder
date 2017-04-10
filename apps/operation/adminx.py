# -*- coding: utf-8 -*-
__author__ = 'lemon'

import xadmin

from .models import UserAsk, FoodComments, UserFavorite, UserMessage, UserFood


class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'food_name', 'add_time']
    search_fields = ['name', 'mobile', 'food_name']
    list_filter = ['name', 'mobile', 'food_name', 'add_time']
    model_icon = 'fa fa-commenting'


class FoodCommentsAdmin(object):
    list_display = ['user', 'food', 'comments', 'add_time']
    search_fields = ['user__username', 'food__name', 'comments']
    list_filter = ['user__username', 'food__name', 'comments', 'add_time']
    model_icon = 'fa fa-comments'


class UserFavoriteAdmin(object):
    list_display = ['user', 'food', 'add_time']
    search_fields = ['user__username', 'food__name']
    list_filter = ['user__username', 'food__name', 'add_time']
    model_icon = 'fa fa-star'


class UserMessageAdmin(object):
    list_display = ['name', 'message', 'has_read', 'add_time']
    search_fields = ['name', 'message']
    list_filter = ['name', 'message', 'has_read', 'add_time']
    model_icon = 'fa fa-bell'


class UserFoodAdmin(object):
    list_display = ['user', 'food']
    search_fields = ['user__username', 'food__name']
    list_filter = ['user__username', 'food__name']
    model_icon = 'fa fa-heart'

xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(FoodComments, FoodCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserFood, UserFoodAdmin)