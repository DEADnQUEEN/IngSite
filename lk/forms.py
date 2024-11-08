from __future__ import annotations
import hashlib
from django import forms
import django.contrib.auth.forms
from . import models
import django.contrib


class UserLogin(forms.Form):
    login = forms.CharField(
        label='Логин, Телефон или Почта',
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


class UserRegister(django.contrib.auth.forms.UserCreationForm):
    login = forms.CharField(
        label='Логин',
        widget=forms.TextInput(
            attrs={
                'class': 'form-input init',
                'id': 'login',
                'placeholder': "Login",
                "minlength": 3,
                "oninput": "on_input_func(this)",
            }
        ),
        error_messages={
            'invalid': "Неправильно заполненное логин пользователя.",
            'unique': "Такой пользователь уже зарегистрирован. Вы можете попробовать его для входа.",
        }
    )
    mail = forms.CharField(
        label='E-mail',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-input init',
                'id': 'mail',
                'placeholder': 'E-Mail',
                "minlength": 4,
                "oninput": "on_input_func(this)",
            }
        ),
        error_messages={
            'invalid': "Неправильно заполнен адрес электронной почты.",
            'unique': "Такая почта уже зарегистрирована в системе.",
        }
    )
    name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(
            attrs={
                'class': 'form-input init',
                'id': 'name',
                'placeholder': 'Имя',
                "minlength": 3,
                "oninput": "on_input_func(this)",
            }
        ),
    )
    surname = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(
            attrs={
                'class': 'form-input init',
                'id': 'surname',
                'placeholder': 'Фамилия',
                "minlength": 3,
                "oninput": "on_input_func(this)",
            }
        ),
    )
    father_name = forms.CharField(
        label='Отчество',
        widget=forms.TextInput(
            attrs={
                'class': 'form-input init',
                'id': 'father-name',
                'placeholder': 'Отчество',
                "minlength": 3,
                "oninput": "on_input_func(this)",
            }
        ),
        error_messages={}
    )
    phone = forms.CharField(
        label='Телефон',
        widget=forms.TextInput(
            attrs={
                'class': 'form-input init',
                'id': 'phone',
                'placeholder': '+71234567890',
                "oninput": "on_input_func(this)",
            }
        ),
        error_messages={
            'unique': "Такой номер телефона уже используется в системе.",
            "required": "Необходимо ввести номер телефона."
        }
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input init',
                'id': 'password',
                'placeholder': 'Пароль',
                'pattern': "[0-9a-zA-Z]{8,}",
                "oninput": "on_input_func(this)",
            }
        ),
        error_messages={
            "required": "Необходимо ввести пароль.",
            'min-length': "Пароль должен быть длиннее 8 символов."
        }
    )
    password2 = forms.CharField(
        label='Проверка Пароля',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input init',
                'id': 'password-check',
                'placeholder': 'Проверка пароля',
                'pattern': "[0-9a-zA-Z]{8,}",
                "oninput": "on_input_func(this)",
            }
        ),
        error_messages={
            "required": "Необходимо подтвердить пароль.",
            'min-length': "Пароль должен быть длиннее 8 символов."
        }
    )

    def save(self, commit=True):
        if self.data['password1'] != self.data['password2']:
            raise ValueError("password is not matched")

        name = models.Human.objects.filter(
            name=self.data['name'],
            surname=self.data['surname'],
            father_name=self.data['father_name']
        ).first()

        if name is None:
            name = models.Human(
                name=self.data['name'],
                surname=self.data['surname'],
                father_name=self.data['father_name']
            )
            name.save()

        user = models.User(
            human=name,
            login=self.data['login'],
            password=hashlib.sha3_256(str(self.data['password1']).encode('UTF-8')).hexdigest(),
            phone=self.data['phone'],
            mail=self.data['mail'],
        )

        user.set_password(self.data['password1'])

        if commit:
            user.save()

        return user

    class Meta:
        model = models.User
        fields = ['login', 'mail', 'name', 'surname', 'father_name', 'phone', 'password1', 'password2']

