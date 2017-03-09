# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.

from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Food


class FoodListView(View):
    def get(self, request):
        all_foods = Food.objects.all().order_by("-add_time")

        # 热门菜 按下单数排序
        hot_foods = Food.objects.all().order_by("-buy_nums")[:3]

        # 对菜单进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_foods, 3, request=request)
        foods = p.page(page)
        return render(request, "food-list.html", {
            "all_foods": foods,
            "hot_foods": hot_foods,
        })