from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.generic.base import View
from cart.forms import CartAddProductForm
from .models import Category, Product


# Create your views here.
class ProductListView(ListView):
    def get(self, request, category_slug=None, ordering='AZ', *args, **kwargs):
        category = None
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
        template_name = 'products/product_list.html'
        context = {'category': category, 'categories': categories, 'products': products}
        return render(request, template_name, context)


class ProductDetailView(View):
    def get(self, request, ordering='AZ', *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs['id'], slug=self.kwargs['slug'], available=True)
        cart_product_form = CartAddProductForm()
        template_name = 'products/product_detail.html'
        context = {'product': product, 'cart_product_form': cart_product_form}
        return render(request, template_name, context)
