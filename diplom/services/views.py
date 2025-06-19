from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ServicePackage, Order, Platform
from .forms import OrderForm
import random
import string

@login_required
def package_list(request):
    packages = ServicePackage.objects.filter(is_active=True)
    popular_packages = packages.filter(is_popular=True)
    
    return render(request, 'services/package_list.html', {
        'packages': packages,
        'popular_packages': popular_packages,
    })

@login_required
def package_detail(request, package_id):
    package = get_object_or_404(ServicePackage, id=package_id, is_active=True)
    
    if request.method == 'POST':
        form = OrderForm(request.POST, package=package)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.package = package
            order.payment_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            order.save()
            
            return redirect('services:payment', order_id=order.id)
    else:
        form = OrderForm(package=package)
    
    return render(request, 'services/package_detail.html', {
        'package': package,
        'form': form,
    })

@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        # Здесь будет обработка "оплаты"
        order.status = 'paid'
        order.save()
        messages.success(request, 'Оплата прошла успешно! Ваш пакет активирован.')
        return redirect('services:order_success', order_id=order.id)
    
    return render(request, 'services/payment.html', {'order': order})

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'services/order_success.html', {'order': order})