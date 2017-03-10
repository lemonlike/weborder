# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.

from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from .models import Food
from operation.models import UserFavorite, FoodComments


class FoodListView(View):
    def get(self, request):
        all_foods = Food.objects.all().order_by("-add_time")

        # 热门菜 按下单数排序
        hot_foods = Food.objects.all().order_by("-buy_nums")[:3]

        # 按菜的类别进行筛选
        category = request.GET.get('ct', '')
        if category:
            all_foods = all_foods.filter(category=category)

        # 按下单数或收藏数排序
        sort = request.GET.get('sort', '')
        if sort == "order":
            all_foods = all_foods.order_by("-buy_nums")
        elif sort == "fav":
            all_foods = all_foods.order_by("-fav_nums")

        # 对菜单进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_foods, 6, request=request)
        foods = p.page(page)
        return render(request, "food-list.html", {
            "all_foods": foods,
            "hot_foods": hot_foods,
            "category": category,
            "sort": sort,
        })


class FoodDetailView(View):
    def get(self, request, food_id):
        food = Food.objects.get(id=int(food_id))

        # 相关菜品推荐（按照类别推荐 并按收藏数排序去前两个）
        category = food.category
        if category:
            relate_foods = Food.objects.filter(category=category).order_by("-fav_nums")[:2]
        else:
            relate_foods = []

        # 传递收藏值
        has_fav_food = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, food_id=food.id):
                has_fav_food = True

        # 显示菜品评论
        food_comments = FoodComments.objects.filter(food_id=food_id).order_by("-add_time")

        return render(request, "food-detail.html", {
            "food": food,
            "relate_foods": relate_foods,
            "has_fav_food": has_fav_food,
            "food_comments": food_comments,
        })


class AddFavView(View):
    """
    用户收藏和取消收藏
    """

    def post(self, request):
        user_id = request.POST.get('user_id', 0)
        food_id = request.POST.get('food_id', 0)

        if not request.user.is_authenticated():
            # 判断用户登陆状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type="application/json")

        exist_records = UserFavorite.objects.filter(user_id=user_id, food_id=food_id)
        if exist_records:
            # 如果记录存在，则表示用户取消收藏
            exist_records.delete()

            # 取消收藏 收藏数减一
            fav_food = Food.objects.get(id=food_id)
            if fav_food.fav_nums > 0:
                fav_food.fav_nums -= 1
                fav_food.save()

            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type="application/json")
        else:
            user_fav = UserFavorite()
            if int(user_id) > 0 and int(food_id) > 0:
                user_fav.user_id = int(user_id)
                user_fav.food_id = int(food_id)
                user_fav.save()

                # 添加收藏 收藏数加一
                fav_food = Food.objects.get(id=food_id)
                if fav_food.fav_nums >= 0:
                    fav_food.fav_nums += 1
                    fav_food.save()

                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type="application/json")
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type="application/json")


class AddCommentsView(View):
    """
    用户添加评论
    """

    def post(self, request):
        if not request.user.is_authenticated():
            # 判断用户登陆状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type="application/json")

        food_id = request.POST.get("food_id", 0)
        comments = request.POST.get("comments", "")
        if food_id > 0 and comments:
            food_comment = FoodComments()
            food = Food.objects.get(id=int(food_id))
            food_comment.user = request.user
            food_comment.food = food
            food_comment.comments = comments
            food_comment.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail", "msg":"评论失败"}', content_type="application/json")
