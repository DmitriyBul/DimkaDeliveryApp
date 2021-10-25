from django.shortcuts import redirect
from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('', lambda req: redirect('/home/')),
    path('home/', views.ProductListView.as_view(), name='product_list'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path('new/', views.NewProductListView.as_view(),
         name='new_product_list'),
    path('ranking/', views.ProductsRankingView.as_view(), name='ranking'),
    path('<slug:category_slug>/', views.ProductListView.as_view(),
         name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]
