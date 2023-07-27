from django import forms

from .models import Pemoran


MAX_CONTENT_LENTGH = 260

class PemoranForm(forms.ModelForm):

    class Meta:
        model = Pemoran
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get('content')

        if len(content) > MAX_CONTENT_LENTGH:
            raise forms.ValidationError('This pemoran is very long')
        else:
            return content