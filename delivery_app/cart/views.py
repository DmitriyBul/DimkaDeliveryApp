from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from accounts.forms import BonusApplyForm
from accounts.models import Profile
from cart.recommender import Recommender
from coupons.forms import CouponApplyForm
from products.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.contrib import messages


@require_POST
@login_required
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
        messages.success(request, 'Товар добавлен в корзину')
    else:
        messages.error(request, 'Произошла ошибка при добавлении товара в корзину')
    return redirect('products:product_list')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, 'Товар удален из корзины')
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
                     'update': True})
    coupon_apply_form = CouponApplyForm()
    bonus_apply_form = BonusApplyForm()
    profile = Profile.objects.get(user=request.user)
    if profile.bonus_scores < cart.bonus_scores:
        messages.error(request, 'Некорректное количество бонусных баллов')
        return redirect(reverse('cart:cart_detail'))
    return render(request, 'cart/detail.html',
                  {'cart': cart, 'coupon_apply_form': coupon_apply_form, 'bonus_apply_form': bonus_apply_form})
