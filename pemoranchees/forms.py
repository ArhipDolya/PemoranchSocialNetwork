from django import forms
from django.conf import settings

from .models import Pemoran


class PemoranForm(forms.ModelForm):

    class Meta:
        model = Pemoran
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get('content')

        if len(content) > settings.MAX_CONTENT_LENGTH:
            raise forms.ValidationError('This pemoran is very long')
        else:
            return content