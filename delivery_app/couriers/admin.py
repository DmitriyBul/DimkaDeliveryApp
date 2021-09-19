from django.contrib import admin

# Register your models here.
from couriers.models import CourierOrder


@admin.register(CourierOrder)
class CourierOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'order']
    search_fields = ('user', 'order')
