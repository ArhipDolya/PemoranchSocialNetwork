from django import forms
from django.conf import settings

from .models import Pemoran


class PemoranForm(forms.ModelForm):

    class Meta:
        model = Pemoran
        fields = ['content']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.user = self.user
        if commit:
            obj.save()
        return obj

    def clean_content(self):
        content = self.cleaned_data.get('content')

        if len(content) > settings.MAX_CONTENT_LENGTH:
            raise forms.ValidationError('This pemoran is very long')
        else:
            return content