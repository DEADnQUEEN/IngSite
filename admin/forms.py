from __future__ import annotations
from django import forms
from lk import models
import hashlib


class UserForm(forms.ModelForm):
    def get_name(self) -> models.Human:
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

        return name

    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'id': 'name',
                'placeholder': "Имя",
                "minlength": 1,
            }
        )
    )
    surname = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'id': 'name',
                'placeholder': "Фамилия",
                "minlength": 1,
            }
        )
    )
    father_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'id': 'name',
                'placeholder': "Отчество",
                "minlength": 1,
            }
        )
    )

    def __init__(self):
        super().__init__()
        fields: list[models.models.Field] = self.Meta.model._meta.get_fields()
        for field in fields:
            if field.name in self.fields.keys():
                self.fields[field.name].widget.attrs.update({
                    'placeholder': field.verbose_name
                })

    class Meta:
        model = models.User
        exclude = ["is_superuser", "groups", "user_permissions", "last_login", "human"]

    def save(self, commit=True):
        name = self.get_name()

        user = self.Meta.model(
            human=name,
            login=self.data['login'],
            password=hashlib.sha3_256(str(self.data['password']).encode('UTF-8')).hexdigest()
        )

        user.set_password(self.data['password'])

        if commit:
            user.save()

        return user


class StudentForm(UserForm):

    class Meta:
        model = models.Student
        fields = "__all__"

    def save(self, commit=True):
        name = self.get_name()

        student = self.Meta.model(
            human=name,
        )

        if commit:
            student.save()

        return student


model_forms = {
    models.User.__name__: UserForm,
    models.Student.__name__: StudentForm,
}

for model_obj in [
    models.Visits, models.Courses, models.Finance, models.Human,
    models.Connect, models.Coins, models.States
]:
    class ModelForm(forms.ModelForm):
        class Meta:
            model = model_obj
            fields = '__all__'

    model_forms[model_obj.__name__] = ModelForm

