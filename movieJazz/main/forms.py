from django import forms

class AddCartForm(forms.Form):
    quantity = forms.IntegerField(required = True)