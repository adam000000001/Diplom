from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Profile

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

#

from django.utils import timezone
from .models import Booking, Computer
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator

# tournament

from .models import Tournament, TournamentRegistration

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email')
    
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date', 'avatar']

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 2*1024*1024:  # 2MB limit
                raise ValidationError(_('Файл слишком большой (максимум 2MB)'))
            return avatar
        
#

class BookingForm(forms.ModelForm):
    computer = forms.ModelChoiceField(
        queryset=Computer.objects.filter(is_active=True),
        label='Выберите компьютер'
    )
    start_time = forms.DateTimeField(
        label='Время начала',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    duration = forms.IntegerField(
        label='Длительность (часы)',
        validators=[MinValueValidator(1), MaxValueValidator(8)],
        initial=1
    )

    class Meta:
        model = Booking
        fields = ['computer', 'start_time', 'duration']

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        duration = cleaned_data.get('duration')
        computer = cleaned_data.get('computer')

        if start_time and duration:
            end_time = start_time + datetime.timedelta(hours=duration)
            
            # Проверка, что бронь в будущем
            if start_time < timezone.now():
                raise ValidationError("Нельзя забронировать компьютер в прошлом")
            
            # Проверка на пересечение с другими бронированиями
            overlapping_bookings = Booking.objects.filter(
                computer=computer,
                start_time__lt=end_time,
                end_time__gt=start_time,
                status__in=['pending', 'confirmed']
            ).exclude(id=self.instance.id if self.instance else None)
            
            if overlapping_bookings.exists():
                raise ValidationError("Этот компьютер уже забронирован на выбранное время")
            
            cleaned_data['end_time'] = end_time
        
        return cleaned_data
    
    #tournament

class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = '__all__'
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date >= end_date:
            raise ValidationError("Дата окончания должна быть позже даты начала")

class TournamentRegistrationForm(forms.ModelForm):
    class Meta:
        model = TournamentRegistration
        fields = []