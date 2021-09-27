from django.urls import path
from . import views

app_name = 'administrators'
urlpatterns = [
    # path('orders/', views.OrderListView.as_view(), name='courier_order_list'),
    path('', views.CategoriesListView.as_view(), name='administrator_page'),
    path('orders/', views.OrdersListView.as_view(), name='orders_list'),
    path('orders/<slug:slug>/', views.ProductsListView.as_view(), name='products_list'),
    path('update/<int:pk>/', views.ProductUpdateView.as_view(), name='update_product'),
    path('delete/<int:pk>/', views.ProductDeleteView.as_view(), name='delete_product'),
    path('add/', views.ProductCreateView.as_view(), name='create_product'),
]
