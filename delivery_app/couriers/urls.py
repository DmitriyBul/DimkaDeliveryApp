from django.urls import path
from . import views

app_name = 'couriers'
urlpatterns = [
    path('products/', views.OrderListView.as_view(), name='courier_order_list'),
]
