from django.urls import path
from . import views

app_name = 'couriers'
urlpatterns = [
    path('orders/', views.OrderListView.as_view(), name='courier_order_list'),
    path('orders/<int:id>/', views.OrderDetailView.as_view(), name='courier_order_detail'),
    path('courierpage/', views.CourierOrderListView.as_view(), name='courier_page'),
    path('orders/<int:id>/completed/', views.ChangeStatusToCompletedView.as_view(), name='change_compl'),
    path('orders/<int:id>/take/', views.AddOrderToCourierView.as_view(), name='take_order'),
]
