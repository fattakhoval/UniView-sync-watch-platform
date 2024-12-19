from django import forms
from django_registration.forms import RegistrationForm
from django.contrib.auth.models import User

class CustomRegistrationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User
        fields = ['email', 'username', 'password1']  # Укажите необходимые поля

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Удалите лишние поля, если они есть
    #