from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column

from .models import ServicePackage

#

from .forms import BookingForm
from .models import Booking, Computer
from django.utils import timezone

# tournament

from .models import Tournament, TournamentRegistration
from .forms import TournamentRegistrationForm

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

#
@login_required
def book_computer(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.end_time = form.cleaned_data['end_time']
            booking.save()
            messages.success(request, 'Компьютер успешно забронирован!')
            return redirect('my_bookings')
    else:
        form = BookingForm()
    
    return render(request, 'accounts/book_computer.html', {'form': form})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-start_time')
    return render(request, 'accounts/my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.start_time > timezone.now() and booking.status in ['pending', 'confirmed']:
        booking.status = 'canceled'
        booking.save()
        messages.success(request, 'Бронирование отменено')
    else:
        messages.error(request, 'Невозможно отменить это бронирование')
    
    return redirect('my_bookings')

    #tournament

def tournament_list(request):
    now = timezone.now()
    upcoming = Tournament.objects.filter(start_date__gt=now, is_active=True).order_by('start_date')
    ongoing = Tournament.objects.filter(start_date__lte=now, end_date__gte=now, is_active=True)
    past = Tournament.objects.filter(end_date__lt=now, is_active=True).order_by('-start_date')[:10]
    
    context = {
        'upcoming_tournaments': upcoming,
        'ongoing_tournaments': ongoing,
        'past_tournaments': past,
    }
    return render(request, 'accounts/tournament_list.html', context)

@login_required
def tournament_detail(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    is_registered = False
    registration = None
    
    if request.user.is_authenticated:
        registration = TournamentRegistration.objects.filter(
            user=request.user,
            tournament=tournament
        ).first()
        is_registered = registration is not None

           # Вычисляем процент заполненности
    if tournament.max_participants > 0:
        percentage = (tournament.registered_count / tournament.max_participants) * 100
    else:
        percentage = 0
    
    if request.method == 'POST':
        if is_registered:
            registration.delete()
            messages.success(request, 'Вы отменили регистрацию на турнир')
        else:
            if tournament.registered_count < tournament.max_participants:
                TournamentRegistration.objects.create(
                    user=request.user,
                    tournament=tournament
                )
                messages.success(request, 'Вы успешно зарегистрировались на турнир!')
            else:
                messages.error(request, 'К сожалению, все места заняты')
        return redirect('tournament_detail', pk=pk)
    
    context = {
        'tournament': tournament,
        'is_registered': is_registered,
        'registration': registration,
        'available_spots': tournament.max_participants - tournament.registered_count,
         'registration_percentage': percentage,
    }
    return render(request, 'accounts/tournament_detail.html', context)

#

def home_view(request):
    # Получаем 3 популярных пакета
    popular_packages = ServicePackage.objects.filter(
        is_active=True, 
        is_popular=True
    )[:3]
    
    # Получаем все активные платформы
    platforms = Platform.objects.all()
    
    context = {
        'popular_packages': popular_packages,
        'platforms': platforms,
    }
    return render(request, 'home.html', context)
