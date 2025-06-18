from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Profile

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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