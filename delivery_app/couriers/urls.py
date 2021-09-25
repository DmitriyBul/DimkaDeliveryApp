from django.urls import path
from . import views

app_name = 'couriers'
urlpatterns = [
    path('orders/', views.OrderListView.as_view(), name='courier_order_list'),
    path('courierpage/', views.CourierOrderListView.as_view(), name='courier_page'),
    path('orders/<int:id>/', views.OrderDetailView.as_view(), name='courier_order_detail'),
    path('orders/compl/<int:id>/', views.ChangeStatusToCompletedView.as_view(), name='change_compl'),
    path('orders/take/<int:id>/', views.AddOrderToCourierView.as_view(), name='take_order'),
]
