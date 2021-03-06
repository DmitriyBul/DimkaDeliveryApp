from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import Profile
from products.models import Product
from products.recommender import Recommender
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            if cart.bonus_scores > 0:
                order.bonus_scores = cart.bonus_scores
            order.user = request.user
            order.first_name = request.user.first_name
            order.email = request.user.email
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])

            r = Recommender()
            cart_products = [item['product'] for item in cart]
            print(cart_products)
            bonus_products = list(Product.objects.filter(name__in=cart_products).values_list('price', flat=True))
            profile = Profile.objects.get(user=request.user)
            if profile.bonus_scores < cart.bonus_scores:
                messages.error(request, 'Некорректное количество бонусных баллов')
                return redirect(reverse('order:create'))
            profile.bonus_scores = profile.bonus_scores - cart.bonus_scores
            if profile.bonus_scores < 0:
                profile.bonus_scores = 0
            scores = profile.bonus_scores
            for item in bonus_products:
                scores += int(int(item) * 0.03)
            profile.bonus_scores = scores
            profile.save()
            main_product = Product.objects.get(name=cart_products[0])
            for item in cart_products[1:]:
                r.products_bought([main_product, item])
            # Очищаем корзину.
            cart.clear()
            request.session['coupon_id'] = None
            request.session['bonus_scores'] = 0
            # Сохранение заказа в сессии.
            request.session['order_id'] = order.id
            # Перенаправление на страницу оплаты.
            messages.success(request, 'Заказ успешно создан')
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})


def order_created(request):
    order_id = request.session.get('order_id')
    return render(request,
                  'orders/order/created.html', {'order_id': order_id})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=\
    "order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(
                                               settings.STATIC_ROOT + 'css/pdf.css')])
    return response
