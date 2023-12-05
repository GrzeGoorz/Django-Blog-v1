from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    # Dodaj dodatkowe pole email do formularza
    email = forms.EmailField()

    class Meta:
        # Określ, że model, na którym ten formularz działa, to User
        model = User
        
        # Określ pola, które mają być uwzględnione w formularzu
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
            email = forms.EmailField()

            class Meta:
                model = User
                fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image'] 
