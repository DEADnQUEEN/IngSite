from __future__ import annotations
from django import forms


class UserLogin(forms.Form):
    login = forms.CharField(
        label='Телефон',
        widget=forms.TextInput(
            attrs={
                'class': 'form-input init',
                'id': 'login',
                'placeholder': "Login",
                "minlength": 3,
                "oninput": "on_input_func(this)",
            }
        )
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input init',
                'id': 'password',
                'placeholder': 'Пароль',
                "minlength": 8,
                "oninput": "on_input_func(this)",
            }
        )
    )

