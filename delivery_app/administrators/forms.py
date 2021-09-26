from django import forms

from products.models import Category, Product


class ProductForm(forms.ModelForm):
    name = forms.CharField(label='Название продукта', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите название продукта'
    }))
    image = forms.ImageField(label='Изображение')
    description = forms.CharField(label='Описание', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите описание продукта'
    }))
    price = forms.DecimalField(label='Цена')
    available = forms.BooleanField(label='В наличии')
    category = forms.ModelChoiceField(
        label='Категория', queryset=Category.objects.all(), widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    class Meta:
        model = Product
        fields = ('name', 'image', 'description', 'price', 'available', 'category')
