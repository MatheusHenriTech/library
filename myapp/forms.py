from django import forms

class BookForm(forms.Form):
    title = forms.CharField(max_length=200)
    author = forms.CharField(max_length=200)
    description = forms.CharField()

    