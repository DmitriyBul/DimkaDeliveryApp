from django.contrib import messages
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views.generic.base import View
from cart.forms import CartAddProductForm
from .recommender import Recommender, r
from .forms import CommentForm, SearchForm
from .models import Category, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
class ProductListView(ListView):
    def get(self, request, category_slug=None, ordering='AZ', *args, **kwargs):
        category = None
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
        lst = Paginator(products, 6)
        page_number = request.GET.get('page')
        page_obj = lst.get_page(page_number)
        template_name = 'products/product_list.html'
        context = {'page_obj': page_obj, 'category': category, 'categories': categories}
        return render(request, template_name, context)


class NewProductListView(ListView):
    def get(self, request, ordering='AZ', *args, **kwargs):
        categories = Category.objects.all()
        products = Product.objects.filter(available=True).order_by('-created')[:12]
        lst = Paginator(products, 6)
        page_number = request.GET.get('page')
        page_obj = lst.get_page(page_number)
        template_name = 'products/new_product_list.html'
        context = {'page_obj': page_obj, 'categories': categories}
        return render(request, template_name, context)


class ProductDetailView(View):
    def get(self, request, ordering='AZ', *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs['id'], slug=self.kwargs['slug'], available=True)
        z = Recommender()
        recommended_products = z.suggest_products_for([product], 3)
        cart_product_form = CartAddProductForm()
        # Увеличиваем количество просмотров товара на 1.
        total_views = r.incr('product:{}:views'.format(product.id))
        r.zincrby('product_ranking', product.id, 1)
        comment_form = CommentForm()
        comments = product.comments.filter(active=True)
        template_name = 'products/product_detail.html'
        context = {'product': product, 'cart_product_form': cart_product_form, 'comments': comments,
                   'comment_form': comment_form, 'recommended_products': recommended_products,
                   'total_views': total_views}
        return render(request, template_name, context)

    def post(self, request, ordering='AZ', *args, **kwargs):
        comment_form = CommentForm(data=request.POST)
        form = CommentForm(request.POST)
        product = get_object_or_404(Product, id=self.kwargs['id'], slug=self.kwargs['slug'], available=True)
        if form.is_valid():
            # Данные формы валидны.
            # img = form.cleaned_data.get("image")
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.product = product
            # Добавляем пользователя к созданному объекту.
            new_item.save()
            messages.success(request, 'Комментарий успешно добавлен')
            return redirect("/")


class SearchResultsView(ListView):
    model = Product
    template_name = 'products/search_results.html'
    category = None
    categories = Category.objects.all()
    context = {'category': category, 'categories': categories}

    def get_queryset(self):  # новый
        query = self.request.GET.get('q')
        product_list = Product.objects.annotate(
            search=SearchVector('name', 'description'),
        ).filter(search=query)
        return product_list


class ProductsRankingView(ListView):
    def get(self, request, ordering='AZ', *args, **kwargs):
        categories = Category.objects.all()
        product_ranking = r.zrange('product_ranking', 0, -1, desc=True)[:10]
        product_ranking_ids = [int(id) for id in product_ranking]
        most_viewed = list(Product.objects.filter(id__in=product_ranking_ids))
        most_viewed.sort(key=lambda x: product_ranking_ids.index(x.id))
        template_name = 'products/products_ranking_results.html'
        context = {'most_viewed': most_viewed, 'categories': categories}
        return render(request, template_name, context)
