from django import forms
from .models import Bread

class BreadForm(forms.ModelForm):
    """
    Form for creating and updating bread
    """

    class Meta:
        model = Bread
        fields = ['name', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }