from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Count

from administrators.forms import ProductForm
from orders.models import Order
from products.models import Category, Product


class CategoriesListView(ListView, LoginRequiredMixin):
    def get(self, request, ordering='AZ', *args, **kwargs):
        categories = Category.objects.all()
        categories = Category.objects.annotate(nprod=Count('products'))
        template_name = 'administrators/categories_list.html'
        context = {'categories': categories}
        return render(request, template_name, context)


class ProductsListView(ListView, LoginRequiredMixin):
    def get(self, request, ordering='AZ', *args, **kwargs):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        products = Product.objects.filter(category=category)
        lst = Paginator(products, 20)
        page_number = request.GET.get('page')
        page_obj = lst.get_page(page_number)
        template_name = 'administrators/products_list.html'
        context = {'page_obj': page_obj, 'products': products}
        return render(request, template_name, context)


class ProductCreateView(CreateView, LoginRequiredMixin, SuccessMessageMixin):
    model = Product
    form_class = ProductForm
    template_name = 'administrators/product/create.html'
    success_message = "Продукт успешно создан"
    success_url = reverse_lazy('administrators:administrator_page')


class ProductUpdateView(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    model = Product
    form_class = ProductForm
    template_name = 'administrators/product/update.html'
    success_message = "Продукт успешно отредактирован"
    success_url = reverse_lazy('administrators:administrator_page')


class ProductDeleteView(LoginRequiredMixin, DeleteView, SuccessMessageMixin):
    model = Product
    success_url = reverse_lazy('administrators:administrator_page')
    success_message = "Продукт успешно удален"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class OrdersListView(ListView, LoginRequiredMixin):
    def get(self, request, ordering='AZ', *args, **kwargs):
        orders = Order.objects.all()
        lst = Paginator(orders, 20)
        page_number = request.GET.get('page')
        page_obj = lst.get_page(page_number)
        template_name = 'administrators/orders_list.html'
        context = {'page_obj': page_obj, 'orders': orders}
        return render(request, template_name, context)
