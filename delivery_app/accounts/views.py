from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.base import View

from orders.models import Order, OrderItem
from .forms import LoginForm, UserRegistrationForm, EmailLoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создаем нового пользователя, но пока не сохраняем в базу данных.
            new_user = user_form.save(commit=False)
            # Задаем пользователю зашифрованный пароль.
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request,
                          'registration/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


# create a function to resolve email to username
def get_user(email):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None


# create a view that authenticate user with email
def email_login(request):
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            username = get_user(email)
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('students:group_list')
                else:
                    return redirect('students:group_list')
            else:
                return redirect('students:group_list')
    else:
        form = EmailLoginForm()
    return render(request, 'account/email_login.html', {'form': form})


class OrderListView(ListView):
    def get(self, request, ordering='AZ', *args, **kwargs):
        orders = Order.objects.filter(user=request.user).order_by('-created')
        template_name = 'account/user_page.html'
        context = {'orders': orders}
        return render(request, template_name, context)


class OrderDetailView(View):
    def get(self, request, ordering='AZ', *args, **kwargs):
        order = get_object_or_404(Order, id=self.kwargs['id'])
        if order.user == request.user:
            products = OrderItem.objects.all()
            products_price = OrderItem.objects.values_list('price', flat=True)
            products_quantity = OrderItem.objects.values_list('quantity', flat=True)
            total = 0
            for i in range(len(products_price)):
                total += float(products_price[i]) * float(products_quantity[i])
        else:
            products = []
            total = 0
        template_name = 'account/order_detail.html'
        context = {'order': order, 'products': products, 'total': total}
        return render(request, template_name, context)
