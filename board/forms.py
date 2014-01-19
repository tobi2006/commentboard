from django import forms
from board.models import *


class SetUpForm(forms.ModelForm):
    class Meta:
        model = Board
        exclude = ('admins', 'open_for', 'opening', 'closing')
        widgets = {
                'title': forms.TextInput(attrs={'class': 'form-control'}),
                'slug': forms.TextInput(attrs={'class': 'form-control'})
            }


