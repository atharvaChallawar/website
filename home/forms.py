# forms.py
from django import forms
from .models import Template

class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ['name', 'pdf_file']
        widgets = {
            'pdf_file': forms.FileInput(attrs={'accept': '.pdf'}),
        }