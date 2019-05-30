from django import forms

class SearchForm(forms.Form):
    input = forms.CharField(max_length = 1000, required = True)