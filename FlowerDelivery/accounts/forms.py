from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django.core.exceptions import ValidationError
import re


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone', 'address')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Этот адрес электронной почты уже занят.")

        # Проверка на корректность формата email (дополнительно, если необходимо)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError("Введите корректный адрес электронной почты.")

        return email

    def save(self, commit=True):
        user = super().save(commit)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(user=user, phone=self.cleaned_data['phone'], address=self.cleaned_data['address'],
                                   email=self.cleaned_data['email'])
        return user