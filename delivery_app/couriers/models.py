from django.conf import settings
from django.db import models


# Create your models here.
from orders.models import Order


class CourierOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='couriers', verbose_name='Курьер',
                             on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order, related_name='orders', on_delete=models.CASCADE)
