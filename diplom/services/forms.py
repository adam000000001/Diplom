from django import forms
from .models import Order, ServicePackage

class OrderForm(forms.ModelForm):
    platform = forms.ModelChoiceField(
        queryset=None,
        widget=forms.RadioSelect,
        empty_label=None,
        label='Выберите платформу'
    )
    
    class Meta:
        model = Order
        fields = ['platform']
    
    def __init__(self, *args, **kwargs):
        package = kwargs.pop('package', None)
        super().__init__(*args, **kwargs)
        if package:
            self.fields['platform'].queryset = package.platforms.all()