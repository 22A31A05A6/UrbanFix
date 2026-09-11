from django import forms
from .models import Complaint


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['issue_type', 'description', 'location', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Describe the issue...'}),
            'location': forms.TextInput(attrs={'placeholder': 'Enter the location'}),
        }
