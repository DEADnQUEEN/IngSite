from django import forms
from django.db import models


class FilterForm(forms.Form):
    def __init__(self, model: models.Model, *args, **kwargs):
        super().__init__(*args, **kwargs)


