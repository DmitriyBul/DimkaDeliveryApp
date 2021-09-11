from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Order
        fields = ['address', 'city']
        exclude = ('first_name', 'email',)
