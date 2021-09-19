from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.generic import ListView
from django.views.generic.base import View

from couriers.models import CourierOrder
from orders.models import Order, OrderItem


class AddOrderToCourierView(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=self.kwargs['id'])
        CourierOrder.objects.get_or_create(user=request.user, order=order)
        return redirect("/couriers/orders/")


class OrderListView(ListView, LoginRequiredMixin):
    def get(self, request, ordering='AZ', *args, **kwargs):
        orders = Order.objects.filter(delivering=False).order_by('-created')
        template_name = 'couriers/courier_order_list.html'
        context = {'orders': orders}
        return render(request, template_name, context)


class OrderDetailView(View):
    def get(self, request, ordering='AZ', *args, **kwargs):
        order = get_object_or_404(Order, id=self.kwargs['id'])
        products = OrderItem.objects.filter(order=order)
        products_price = products.values_list('price', flat=True)
        products_quantity = products.values_list('quantity', flat=True)
        total = 0
        for i in range(len(products_price)):
            total += float(products_price[i]) * float(products_quantity[i])

        template_name = 'couriers/courier_order_detail.html'
        context = {'order': order, 'products': products, 'total': total}
        return render(request, template_name, context)
