from django import forms
from .models import Profile

class BookForm(forms.Form):
    title = forms.CharField(max_length=200)
    author = forms.CharField(max_length=200)
    description = forms.CharField()


class ProfileForm(forms.ModelForms):
    class Meta:
        model = Profile
        fields = ['photo']
