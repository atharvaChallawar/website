# forms.py
from django import forms
from .models import template

class TemplateForm(forms.ModelForm):
    class Meta:
        model = template
        fields = ['name', 'pdf_file']
        widgets = {
            'pdf_file': forms.FileInput(attrs={'accept': '.pdf'}),
        }