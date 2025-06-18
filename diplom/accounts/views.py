from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column

from .models import ServicePackage

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} был создан! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# @login_required
# def profile(request):
#     return render(request, 'accounts/profile.html')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Ваш профиль обновлен!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'accounts/profile.html', context)

#Service

def home(request):
    packages = ServicePackage.objects.all()
    popular_packages = ServicePackage.objects.filter(is_popular=True)
    
    context = {
        'packages': packages,
        'popular_packages': popular_packages
    }
    return render(request, 'home.html', context)
