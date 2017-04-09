# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.

from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q

from .models import Food, ShopCart, Room, Order, OrderDetail
from operation.models import UserFavorite, FoodComments, UserFood
from utils.mixin_utils import LoginRequiredMixin


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

        # 菜品全局搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_foods = all_foods.filter(name__icontains=search_keywords)

        # 对菜单进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_foods, 9, request=request)
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
            relate_foods = Food.objects.filter(Q(category=category), ~Q(id=int(food_id))).order_by("-fav_nums")[:2]
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


class AddShopCartView(LoginRequiredMixin, View):
    """
    加入购物车
    """

    def get(self, request, food_id):
        shop_cart = ShopCart()

        # 统计数量
        exist_foods = ShopCart.objects.filter(food_id=food_id)
        if exist_foods:
            for exist_food in exist_foods:
                exist_food.quantity += 1
                exist_food.save()
        else:
            shop_cart.user = request.user
            shop_cart.food_id = food_id
            shop_cart.save()
        return HttpResponseRedirect(reverse('food:food_detail', kwargs={'food_id': int(food_id)}))


class ShopCartView(LoginRequiredMixin, View):
    """
    购物车详情页
    """

    def get(self, request):
        # 取得购物车记录
        shop_carts = ShopCart.objects.filter(user=request.user)

        # 计算订单总价格
        total_price = 0
        for shop_cart in shop_carts:
            total_price += shop_cart.augment_price()

        # 取得包间记录
        rooms = Room.objects.filter(has_order=False)
        return render(request, "shopping-cart.html", {
            "shop_carts": shop_carts,
            "rooms": rooms,
            "total_price": total_price
        })


class ShopCartDeleteView(View):
    """
    购物车删除
    """

    def get(self, request, delete_id):
        delete_food = ShopCart.objects.filter(user=request.user, food_id=delete_id)
        if delete_food:
            delete_food.delete()
            return HttpResponseRedirect(reverse("food:shop_cart"))


class ConfirmOrder(View):
    """
    确认订单
    """

    def post(self, request):
        total_money = request.POST.get("total_price", '')
        preset_time = request.POST.get("preset_time", '')
        room_num = request.POST.get("room_num", '')

        # 存储订单数据
        order = Order()
        order.user = request.user
        order.total_money = total_money
        order.preset_time = preset_time
        order.room_num = room_num
        order.save()

        # 包间已预订
        # order_rooms = Room.objects.filter(name=room_num)
        # if order_rooms:
        #     for order_room in order_rooms:
        #         order_room.has_order = True
        #         order_room.save()

        # 存储订单详情数据
        order_detail = OrderDetail()
        # 存储用户点过的菜
        user_food = UserFood()

        shop_carts = ShopCart.objects.filter(user=request.user)
        # 每次存数据时，先确定detail_id的起始值
        order_detail.detail_id = OrderDetail.objects.all().count()
        # 每次存数据时，先确定user_food_id的起始值
        user_food.user_food_id = UserFood.objects.all().count()

        for shop_cart in shop_carts:
            order_detail.detail_id += 1
            order_detail.order_id = order.id
            order_detail.food = shop_cart.food
            order_detail.quantity = shop_cart.quantity
            # 菜品下单数自增
            food = Food.objects.get(id=order_detail.food_id)
            food.buy_nums += order_detail.quantity
            food.save()
            order_detail.save()

            # 用户点过的菜
            has_order_food = UserFood.objects.filter(food_id=shop_cart.food_id)
            if has_order_food:
                pass
            else:
                user_food.user_food_id += 1
                user_food.user = request.user
                user_food.food_id = shop_cart.food_id
                user_food.save()

        shop_carts.all().delete()

        return render(request, "shopping-pay.html", {
            "total_money": total_money,
            "order_id": order.id
        })


class CompletePayView(View):
    """
    完成支付
    """

    def post(self, request):
        order_id = request.POST.get("order_id", '')
        orders = Order.objects.filter(id=order_id)
        if orders:
            for order in orders:
                order.has_pay = True
                order.save()
            return HttpResponseRedirect(reverse("index"))


class MyOrderView(LoginRequiredMixin, View):
    """
    我的订单
    """

    def get(self, request):
        my_orders = Order.objects.filter(user=request.user).order_by("-order_time")
        return render(request, "shopping-order.html", {
            "my_orders": my_orders,
        })


class MyOrderDetail(View):
    """
    订单详情
    """

    def get(self, request, order_id):
        order_details = OrderDetail.objects.filter(order_id=order_id)
        return render(request, "shopping-order-detail.html", {
            "order_details": order_details
        })
